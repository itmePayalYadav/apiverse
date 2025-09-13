# User Roles
ROLE_USER = "USER"
ROLE_ADMIN = "ADMIN"

ROLE_CHOICES = [
    (ROLE_USER, "User"),
    (ROLE_ADMIN, "Admin"),
]

# Login Types
LOGIN_EMAIL_PASSWORD = "EMAIL_PASSWORD"
LOGIN_GOOGLE = "GOOGLE"
LOGIN_GITHUB = "GITHUB"

LOGIN_TYPE_CHOICES = [
    (LOGIN_EMAIL_PASSWORD, "Email & Password"),
    (LOGIN_GOOGLE, "Google"),
    (LOGIN_GITHUB, "GitHub"),
]

# Todo List Priority
PRIORITY_LOW = "low"
PRIORITY_MEDIUM = "medium"
PRIORITY_HIGH = "high"

PRIORITY_CHOICES = [
    (PRIORITY_LOW, "Low"),
    (PRIORITY_MEDIUM, "Medium"),
    (PRIORITY_HIGH, "High"),
]
