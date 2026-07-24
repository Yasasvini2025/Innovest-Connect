# Innovest Connect

Innovest Connect is a web-based **Startup–Investor Platform** designed to connect startups with potential investors. The platform provides separate workflows for startups and investors, allowing users to register, log in, explore startup projects, post project information, view project details, and manage their profiles.

## Features

### User Authentication
- User registration and login
- Forgot password workflow
- OTP verification workflow
- Password reset workflow
- Session-based authentication

### Startup Features
- Startup dashboard
- Post startup/project information
- Edit project details
- View posted projects
- Upload project documents

### Investor Features
- Investor dashboard
- Browse startup/project opportunities
- View detailed project information
- Explore projects posted by startups

### Project Management
- Project posting and editing
- Project detail pages
- Project document uploads
- Separate startup and investor dashboards

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML | Web page structure |
| CSS | Styling and UI design |
| JavaScript | Client-side functionality |
| JSON | Local data storage |
| Jinja2 | Dynamic HTML templates |

## Project Structure

```text
Innovest-Connect/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── about.html
    ├── edit_project.html
    ├── forgot_password.html
    ├── home.html
    ├── investor_dashboard.html
    ├── login.html
    ├── project_post.html
    ├── project_view.html
    ├── register.html
    ├── reset_otp.html
    ├── reset_password.html
    ├── startup_dashboard.html
    ├── verify_otp.html
    └── view_project.html
```

> The original project also contains local data files and an upload directory. Do not commit real user information, passwords, private documents, or other sensitive data to a public repository.

## Prerequisites

- Python 3.x
- pip
- Git (optional)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Innovest-Connect.git
cd Innovest-Connect
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Review the configuration in `app.py` before running the application.

For a public GitHub repository:

- Do not hard-code secret keys.
- Do not commit real passwords.
- Do not commit email credentials or API keys.
- Store sensitive values in environment variables or a `.env` file.
- Keep `.env` excluded using `.gitignore`.

Keep uploaded user documents out of the public repository.

## Running the Application

Run:

```bash
python app.py
```

Then open the local address shown by Flask, commonly:

```text
http://127.0.0.1:5000/
```

## Application Workflow

1. Register as a startup or investor.
2. Log in to your account.
3. Startups can access their dashboard and post project information.
4. Investors can access their dashboard and explore projects.
5. Users can view project details.
6. Startups can edit project information.
7. Project documents can be handled through the upload functionality.
8. Users can use password recovery and OTP verification when required.

## Data and Privacy

The original implementation uses local JSON files for application data.

For a public GitHub repository, do not upload:

- Real user accounts
- User passwords
- Private user information
- Private startup documents
- Confidential investor information
- Secret keys or credentials

Use sample/demo data when publishing the project for academic or portfolio purposes.

## Future Enhancements

- Replace JSON storage with MySQL or PostgreSQL
- Add secure password hashing
- Implement production-ready email OTP delivery
- Add investor-startup messaging
- Add investor interest or funding requests
- Add advanced project search and filtering
- Add secure cloud document storage
- Add role-based authorization
- Improve security and input validation

## Disclaimer

Innovest Connect is an academic/portfolio project created to demonstrate a startup-investor platform concept. It should be reviewed and secured further before being used with real users or sensitive data.

## Author

**Kala**

MCA Student
