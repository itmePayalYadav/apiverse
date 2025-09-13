from .models import User
from rest_framework import serializers
from core.constants import ROLE_CHOICES

# ----------------------------
# Register Serializer
# ----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

# ----------------------------
# Verify Email Serializer
# ----------------------------
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

# ----------------------------
# Login Serializer
# ----------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# ----------------------------
# Forgot Password Serializer
# ----------------------------
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# ----------------------------
# Reset Password Serializer
# ----------------------------
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)

# ----------------------------
# Change Password Serializer
# ----------------------------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "is_verified", "avatar_url"]

# ----------------------------
# Resend Email Verification
# ----------------------------
class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No account found with this email.")

        if user.is_verified:  
            raise serializers.ValidationError("This email is already verified.")

        self.context["user"] = user
        return value

    def validate(self, attrs):
        attrs["user"] = self.context["user"]
        return attrs
    
# ----------------------------
# Update Avatar Serializer
# ----------------------------
class UpdateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar"]

# ----------------------------
# Change Role Serializer
# ----------------------------
class ChangeRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

# ----------------------------
# OAuth Callback Serializers
# ----------------------------
class OAuthCallbackSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)