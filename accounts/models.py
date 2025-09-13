import time
import uuid
import secrets
import hashlib
import jwt
from core.models import BaseModel
from django.db import models
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from .managers import UserManager, ActiveUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.constants import ROLE_CHOICES, LOGIN_TYPE_CHOICES, ROLE_USER, LOGIN_EMAIL_PASSWORD

def avatar_upload_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ROLE_USER)
    login_type = models.CharField(max_length=50, choices=LOGIN_TYPE_CHOICES, default=LOGIN_EMAIL_PASSWORD)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    refresh_token = models.TextField(blank=True, null=True)
    forgot_password_token = models.CharField(max_length=255, blank=True, null=True)
    forgot_password_expiry = models.DateTimeField(blank=True, null=True)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_expiry = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()
    active_objects = ActiveUserManager()

    # ----------------------------
    # Avatar URL
    # ----------------------------
    @property
    def avatar_url(self):
        if self.avatar:
            try:
                return self.avatar.url
            except ValueError:
                return None
        name = self.username.replace(" ", "+")
        return f"https://ui-avatars.com/api/?name={name}&size=200"

    # ----------------------------
    # String representation
    # ----------------------------
    def __str__(self):
        return self.email

    # ----------------------------
    # Soft delete
    # ----------------------------
    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    # ----------------------------
    # JWT tokens
    # ----------------------------
    def generate_access_token(self, minutes=15):
        exp_timestamp = int(time.time()) + minutes * 60
        payload = {"id": str(self.id), "email": self.email, "username": self.username, "role": self.role, "exp": exp_timestamp}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def generate_refresh_token(self, days=7):
        exp_timestamp = int(time.time()) + days * 24 * 60 * 60
        payload = {"id": str(self.id), "exp": exp_timestamp}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # ----------------------------
    # Temporary token generator
    # ----------------------------
    def generate_temporary_token(self, expiry_minutes=20):
        un_hashed = secrets.token_hex(20)
        hashed = hashlib.sha256(un_hashed.encode()).hexdigest()
        expiry = timezone.now() + timedelta(minutes=expiry_minutes)
        return un_hashed, hashed, expiry
    