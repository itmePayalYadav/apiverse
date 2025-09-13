import secrets
import hashlib
from datetime import timedelta
from threading import Thread
import logging
from smtplib import SMTPException

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

from typing import Optional, Union

from accounts.emails import EMAIL_TEMPLATES

logger = logging.getLogger(__name__)

# ----------------------------
# Generate Temporary Token
# ----------------------------
def generate_temporary_token(expiry_minutes: int = 20):
    """
    Generates a secure temporary token with an expiry time.
    Returns:
        un_hashed: str - token to send to user
        hashed: str - hashed token to store in DB
        expiry: datetime - expiry timestamp
    """
    un_hashed = secrets.token_hex(20)
    hashed = hashlib.sha256(un_hashed.encode()).hexdigest()
    expiry = timezone.now() + timedelta(minutes=expiry_minutes)
    return un_hashed, hashed, expiry

# ----------------------------
# Standardized API Response
# ----------------------------
def api_response(
    success: bool,
    message: str,
    data: Optional[Union[dict, list]] = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Returns a standardized API response for DRF views.

    Args:
        success (bool): True/False
        message (str): Human-readable message
        data (dict | list, optional): Payload data
        status_code (int, optional): HTTP status code (default: 200)

    Returns:
        Response: DRF Response object
    """
    response = {
        "success": success,
        "message": message,
        "data": data or {},
    }
    return Response(response, status=status_code)

# ----------------------------
# Synchronous Template-based Email Sender
# ----------------------------
def _send_email_sync(to_email: str, subject: str, template_name: str = "generic", context: dict = None):
    """
    Internal function to send an email synchronously using a template.
    Raises exception if email fails to send.
    """
    from_email = getattr(settings, "EMAIL_FROM", None)
    if not from_email:
        raise ValueError("EMAIL_FROM is not configured in settings.")

    template = EMAIL_TEMPLATES.get(template_name, EMAIL_TEMPLATES["generic"])
    context = context or {}
    
    try:
        message = template.format(**context)
    except KeyError as e:
        raise ValueError(f"Missing context key for email template: {e}")

    try:
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        logger.info(f"Email sent to {to_email}")
    except SMTPException as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise Exception("Failed to send email.")

# ----------------------------
# Asynchronous Template-based Email Sender
# ----------------------------
def send_email(to_email: str, subject: str, template_name: str = "generic", context: dict = None):
    """
    Public function to send an email asynchronously using a thread.
    Usage examples:
        send_email("user@example.com", "Welcome!", "welcome", {"username": "John"})
        send_email("user@example.com", "Reset Password", "reset_password", {"username": "John", "reset_link": "link"})
    """
    Thread(
        target=_send_email_sync,
        args=(to_email, subject, template_name, context),
        daemon=True
    ).start()
