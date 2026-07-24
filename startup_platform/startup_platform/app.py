from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import os
import json
import time
import random
import string
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------------- File Setup ----------------------
USERS_FILE = "users.json"
PROJECTS_FILE = "projects.json"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_users():
    return json.load(open(USERS_FILE)) if os.path.exists(USERS_FILE) else {}

def save_users():
    json.dump(users, open(USERS_FILE, "w"), indent=4)

def load_projects():
    return json.load(open(PROJECTS_FILE)) if os.path.exists(PROJECTS_FILE) else []

def save_projects():
    json.dump(projects, open(PROJECTS_FILE, "w"), indent=4)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

users = load_users()
projects = load_projects()

# ---------------------- Utility ----------------------
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_email_otp(email, otp):
    print("OTP sent:", otp)

def strong_password(pwd):
    return (
        len(pwd) >= 8
        and re.search(r"[A-Z]", pwd)
        and re.search(r"[0-9]", pwd)
        and re.search(r"[@$!%*?&]", pwd)
    )

# ---------------------- Home ----------------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------------- About ----------------------
    
@app.route('/about')
def about():
    return render_template('about.html')

# ---------------------- Register / OTP ----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        user_type = request.form["user_type"]

        if username in users:
            flash("Username already exists.")
            return redirect(url_for("register"))

        if not strong_password(password):
            flash("Weak password.")
            return redirect(url_for("register"))

        otp = generate_otp()
        users[username] = {
            "email": email,
            "password": password,
            "user_type": user_type,
            "is_verified": False,
            "otp": otp,
            "otp_time": time.time(),
            "resend_count": 0
        }
        save_users()
        send_email_otp(email, otp)
        flash("Verify email to continue.")
        return redirect(url_for("verify_otp", username=username))

    return render_template("register.html")

@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    username = request.args.get("username")
    if not username or username not in users:
        return redirect(url_for("register"))

    user = users[username]
    expired = time.time() - user["otp_time"] > 300

    if request.method == "POST":
        if expired:
            flash("OTP expired.")
            return redirect(url_for("verify_otp", username=username))

        if request.form["otp"] == user["otp"]:
            user["is_verified"] = True
            user["otp"] = None
            save_users()
            flash("Verified. Login now.")
            return redirect(url_for("login"))

        flash("Incorrect OTP.")

    return render_template("verify_otp.html", username=username, expired=expired)

# ---------------------- Login ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_type = request.form["user_type"]

        user = users.get(username)

        if not user or user["password"] != password or not user["is_verified"] or user["user_type"] != user_type:
            flash("Invalid login.")
            return redirect(url_for("login"))

        session["username"] = username
        session["user_type"] = user_type

        return redirect(url_for("startup_dashboard" if user_type == "startup" else "investor_dashboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("home"))

# ---------------------- Dashboards ----------------------
@app.route("/startup_dashboard")
def startup_dashboard():
    if session.get("user_type") != "startup":
        return redirect(url_for("login"))
    return render_template("startup_dashboard.html", projects=projects)

@app.route("/investor_dashboard")
def investor_dashboard():
    if session.get("user_type") != "investor":
        return redirect(url_for("login"))
    return render_template("investor_dashboard.html", projects=projects)

# ---------------------- Uploads ----------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---------------------- POST PROJECT ----------------------
@app.route("/project_post", methods=["GET", "POST"])
def project_post():
    if session.get("user_type") != "startup":
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("title")
        domain = request.form.get("domain")
        desc = request.form.get("description")

        # registered email
        email = users[session["username"]]["email"]

        # contact email written in form
        contact_email = request.form.get("contact_email")

        if not name or not domain or not contact_email:
            flash("Please fill all required fields.")
            return redirect(url_for("project_post"))

        file = request.files.get("abstract")
        if not file or not allowed_file(file.filename):
            flash("Upload PDF/DOC/DOCX.")
            return redirect(url_for("project_post"))

        filename = secure_filename(f"{session['username']}_{name}_{file.filename}")
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        projects.append({
            "username": session["username"],
            "name": name,
            "domain": domain,
            "desc": desc,
            "email": email,                  # stored main email
            "contact_email": contact_email,  # visible email
            "file": filename
        })

        save_projects()
        flash("Project posted successfully.")
        return redirect(url_for("project_view"))

    return render_template("project_post.html")



# ---------------------- FIXED PROJECT VIEW (GROUPED + FILTERS + DOMAINS) ----------------------
@app.route("/project_view")
def project_view():
    if "username" not in session:
        return redirect(url_for("login"))

    domain_filter = request.args.get("domain")
    search_query = request.args.get("search", "").strip().lower()

    # investors see all projects, startups see only their own
    if session.get("user_type") == "startup":
        filtered = [p for p in projects if p.get("username") == session["username"]]
    else:
        filtered = projects.copy()

    # filter by domain if selected
    if domain_filter:
        filtered = [p for p in filtered if p.get("domain") == domain_filter]

    # filter by search query
    if search_query:
        filtered = [
            p for p in filtered
            if search_query in p.get("name", "").lower() or search_query in p.get("desc", "").lower()
        ]

    # safely collect all domains
    all_domains = sorted(list({p.get("domain", "Other") for p in filtered}))

    return render_template(
        "project_view.html",
        projects=filtered,
        all_domains=all_domains,
        search_query=search_query,
        domain_filter=domain_filter
    )




# ---------------------- VIEW SINGLE PROJECT ----------------------
@app.route("/view_project/<project_name>")
def view_project(project_name):
    if "username" not in session:
        return redirect(url_for("login"))

    if session.get("user_type") == "startup":
        proj = next((p for p in projects if p["username"] == session["username"] and p["name"] == project_name), None)
    else:
        proj = next((p for p in projects if p["name"] == project_name), None)

    if not proj:
        flash("Project not found.")
        return redirect(url_for("project_view"))

    return render_template("view_project.html", project=proj)


# ---------------------- Delete Project ----------------------
@app.route("/delete_project", methods=["POST"])
def delete_project():
    if session.get("user_type") != "startup":
        return redirect(url_for("login"))

    name = request.form.get("project_name")
    global projects
    projects = [p for p in projects if not (p["username"] == session["username"] and p["name"] == name)]
    save_projects()
    flash("Project deleted.")
    return redirect(url_for("project_view"))

# ---------------------- Edit Project ----------------------
@app.route("/edit_project", methods=["GET", "POST"])
def edit_project():
    if session.get("user_type") != "startup":
        return redirect(url_for("login"))

    if request.method == "GET":
        name = request.args.get("project_name")
        proj = next((p for p in projects if p["username"] == session["username"] and p["name"] == name), None)
        if not proj:
            flash("Project missing.")
            return redirect(url_for("project_view"))
        return render_template("edit_project.html", project=proj)

    old = request.form.get("old_name")
    new = request.form.get("project_name")
    desc = request.form.get("project_desc")
    domain = request.form.get("domain")

    for p in projects:
        if p["username"] == session["username"] and p["name"] == old:
            p["name"] = new
            p["desc"] = desc
            p["domain"] = domain
            break

    save_projects()
    flash("Updated.")
    return redirect(url_for("project_view"))

# ---------------------- Run ----------------------
if __name__ == "__main__":
    app.run(debug=True)
