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
PRIORITY_LOW = "Low"
PRIORITY_MEDIUM = "Medium"
PRIORITY_HIGH = "High"

PRIORITY_CHOICES = [
    (PRIORITY_LOW, "Low"),
    (PRIORITY_MEDIUM, "Medium"),
    (PRIORITY_HIGH, "High"),
]

# Coupon Types
FLAT = "FLAT"
PERCENTAGE = "PERCENTAGE"

COUPON_TYPES = [
    (FLAT, "Flat"),
    (PERCENTAGE, "Percentage"),
]

# Order Status
PENDING = "PENDING"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"

ORDER_STATUS = [
    (PENDING, "Pending"),
    (COMPLETED, "Completed"),
    (CANCELLED, "Cancelled"),
]

# Payment Providers
RAZORPAY = "RAZORPAY"
STRIPE = "STRIPE"

PAYMENT_PROVIDERS = [
    (RAZORPAY, "Razorpay"),
    (STRIPE, "Stripe"),
]
