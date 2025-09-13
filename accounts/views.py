import urllib.parse
from rest_framework import generics, status, permissions
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
import jwt, hashlib, secrets, requests
from .models import User
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    UserSerializer,
    ForgotPasswordSerializer, 
    ResetPasswordSerializer, 
    ChangePasswordSerializer,
    VerifyEmailSerializer,
    ResendEmailVerificationSerializer,
    UpdateAvatarSerializer,
    ChangeRoleSerializer,
    OAuthCallbackSerializer
)
from core.utils import send_email, api_response
from .permissions import IsAdminOrStaffOrSuperuser
from core.constants import LOGIN_GOOGLE, LOGIN_GITHUB

# ----------------------
# Register with email verification
# ----------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        un_hashed = secrets.token_hex(20)
        hashed = hashlib.sha256(un_hashed.encode()).hexdigest()
        expiry = timezone.now() + timezone.timedelta(minutes=10)

        user.email_verification_token = hashed
        user.email_verification_expiry = expiry
        user.save(update_fields=["email_verification_token", "email_verification_expiry"])

        verify_link = f"{settings.FRONTEND_URL}/verify-email/{un_hashed}"
        send_email(
            to_email=user.email,
            subject="Verify your email",
            template_name="email_verification",
            context={"username": user.username, "verification_code": un_hashed}
        )

        return api_response(
            success=True,
            message="User registered successfully. Please verify your email.",
            data={"user": UserSerializer(user).data},
            status_code=status.HTTP_201_CREATED
        )

# ----------------------
# Verify Email
# ----------------------
class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        hashed_token = hashlib.sha256(token.encode()).hexdigest()

        user = User.objects.filter(
            email_verification_token=hashed_token,
            email_verification_expiry__gt=timezone.now()
        ).first()

        if not user:
            return api_response(success=False, message="Invalid or expired token", status_code=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.email_verification_token = None
        user.email_verification_expiry = None
        user.save(update_fields=["is_verified", "email_verification_token", "email_verification_expiry"])

        return api_response(success=True, message="Email verified successfully")

# ----------------------
# Login
# ----------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(email=serializer.validated_data["email"], password=serializer.validated_data["password"])
        if not user:
            return api_response(success=False, message="Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return api_response(success=False, message="Email not verified", status_code=status.HTTP_403_FORBIDDEN)

        access_token = user.generate_access_token()
        refresh_token = user.generate_refresh_token()
        user.refresh_token = refresh_token
        user.save(update_fields=["refresh_token"])

        return api_response(
            success=True,
            message="Login successful",
            data={"user": UserSerializer(user).data, "access": access_token, "refresh": refresh_token},
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Logout
# ----------------------
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.refresh_token = None
        request.user.save(update_fields=["refresh_token"])
        return api_response(success=True, message="Logged out successfully")

# ----------------------
# Refresh token
# ----------------------
class RefreshTokenView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return api_response(success=False, message="Refresh token required", status_code=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"], refresh_token=refresh)
            access = user.generate_access_token()
            return api_response(success=True, message="Access token generated", data={"access": access})
        except:
            return api_response(success=False, message="Invalid refresh token", status_code=status.HTTP_400_BAD_REQUEST)

# ----------------------
# Forgot Password
# ----------------------
class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()

        if user:
            un_hashed = secrets.token_hex(20)
            hashed = hashlib.sha256(un_hashed.encode()).hexdigest()
            expiry = timezone.now() + timezone.timedelta(minutes=10)

            user.forgot_password_token = hashed
            user.forgot_password_expiry = expiry
            user.save(update_fields=["forgot_password_token", "forgot_password_expiry"])

            reset_link = f"{settings.FRONTEND_URL}/reset-password/{un_hashed}"
            send_email(to_email=user.email, subject="Reset Password", template_name="reset_password",
                    context={"username": user.username, "reset_link": reset_link})

        return api_response(success=True, message="Reset link sent succesfully.")

# ----------------------
# Reset Password
# ----------------------
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        user = User.objects.filter(forgot_password_token=hashed_token, forgot_password_expiry__gt=timezone.now()).first()

        if not user:
            return api_response(success=False, message="Invalid or expired token", status_code=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.forgot_password_token = None
        user.forgot_password_expiry = None
        user.save(update_fields=["password", "forgot_password_token", "forgot_password_expiry"])

        return api_response(success=True, message="Password reset successful")

# ----------------------
# Change Password
# ----------------------
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(serializer.validated_data["old_password"]):
            return api_response(success=False, message="Old password incorrect", status_code=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return api_response(success=True, message="Password changed successfully")

# ----------------------
# Resend Email Verificaiton
# ----------------------
class ResendEmailVerificationView(generics.GenericAPIView):
    serializer_class = ResendEmailVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        un_hashed = secrets.token_hex(20)
        hashed = hashlib.sha256(un_hashed.encode()).hexdigest()
        expiry = timezone.now() + timezone.timedelta(minutes=10)

        user.email_verification_token = hashed
        user.email_verification_expiry = expiry
        user.save(update_fields=["email_verification_token", "email_verification_expiry"])

        verify_link = f"{settings.FRONTEND_URL}/verify-email/{un_hashed}"

        send_email(
            to_email=user.email,
            subject="Verify your email",
            template_name="email_verification",
            context={
                "username": user.username,
                "verification_code": un_hashed,  
                "verify_link": verify_link,
            },
        )

        return api_response(
            success=True,
            message="Verification email resent successfully.",
            status_code=status.HTTP_200_OK,
        )        

# ----------------------
# Current User
# ----------------------
class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_response(
            success=True,
            message="Current user retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Update Avatar
# ----------------------
class UpdateAvatarView(generics.UpdateAPIView):
    serializer_class = UpdateAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            success=True,
            message="Avatar updated successfully",
            data={"avatar": request.user.avatar_url},
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Google OAuth Login
# ----------------------
class GoogleLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        google_client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = urllib.parse.quote(settings.GOOGLE_REDIRECT_URI)
        scope = urllib.parse.quote("openid email profile")

        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"response_type=code&client_id={google_client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            f"&access_type=offline&prompt=consent"
        )

        return api_response(
            success=True,
            message="Google login URL generated successfully",
            data={"auth_url": auth_url},
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Google OAuth Login Callback
# ----------------------
class GoogleLoginCallbackView(generics.GenericAPIView):
    serializer_class = OAuthCallbackSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_res = requests.post(token_url, data=data).json()
        google_access_token = token_res.get("access_token")

        if not google_access_token:
            return api_response(
                success=False,
                message="Failed to get access token from Google",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {google_access_token}"}
        user_info = requests.get(user_info_url, headers=headers).json()

        email = user_info.get("email")
        name = user_info.get("name")

        if not email:
            return api_response(
                success=False,
                message="Email not available from Google",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": name, "is_verified": True, "login_type": LOGIN_GOOGLE}
        )
        if not created:
            user.username = name
            user.is_verified = True
            user.save(update_fields=["username", "is_verified"])

        access = user.generate_access_token()
        refresh = user.generate_refresh_token()
        user.refresh_token = refresh
        user.save(update_fields=["refresh_token"])

        return api_response(
            success=True,
            message="Login successful",
            data={
                "user": UserSerializer(user).data,
                "access": access,
                "refresh": refresh,
            },
            status_code=status.HTTP_200_OK,
        )

# ----------------------
# GitHub OAuth Login
# ----------------------
class GitHubLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = settings.GITHUB_REDIRECT_URI
        auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user:email"
        
        return api_response(
            success=True,
            message="Github login URL generated successfully",
            data={"auth_url": auth_url},
            status_code=status.HTTP_200_OK
        )

# ----------------------
# GitHub OAuth Login Callback
# ----------------------
class GitHubLoginCallbackView(generics.GenericAPIView):
    serializer_class = OAuthCallbackSerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        token_url = "https://github.com/login/oauth/access_token"
        data = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        }
        headers = {"Accept": "application/json"}
        token_res = requests.post(token_url, data=data, headers=headers).json()

        access_token = token_res.get("access_token")
        if not access_token:
            return api_response(
                success=False,
                message="Failed to get access token from GitHub",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user_info_url = "https://api.github.com/user"
        headers = {"Authorization": f"token {access_token}"}
        user_info = requests.get(user_info_url, headers=headers).json()

        email = user_info.get("email")
        username = user_info.get("login")

        if not email:
            email = f"{user_info.get('id')}@github.com"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "is_verified": True,
                "login_type": LOGIN_GITHUB
            }
        )
        if not created:
            user.username = username
            user.is_verified = True
            user.save(update_fields=["username", "is_verified"])

        access = user.generate_access_token()
        refresh = user.generate_refresh_token()
        user.refresh_token = refresh
        user.save(update_fields=["refresh_token"])

        return api_response(
            success=True,
            message="User login successful",
            data={
                "user": UserSerializer(user).data,
                "access": access,
                "refresh": refresh,
            },
            status_code=status.HTTP_200_OK,
        )

# ----------------------
# Role Management
# ----------------------
class ChangeRoleView(generics.GenericAPIView):
    serializer_class = ChangeRoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStaffOrSuperuser]
    
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_role = serializer.validated_data["role"]
        user = request.user
        
        user.role = new_role
        user.save(update_fields=["role"])
        
        return api_response(
            success=True,
            message=f"Role updated successfully to {new_role}",
            data={"role": user.role},
            status_code=status.HTTP_200_OK
        )
