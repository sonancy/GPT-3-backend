from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from .models import User
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils import timezone
from .emailTemplates.verifyEmail import emailVerifyTemplate
from .emailTemplates.resetPassword import resetPasswordTemplate
from .token import account_activation_token, password_reset_token
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)
        link = f'http://localhost:3000/auth/verify-email?uid={uid}&token={token}'
        html = emailVerifyTemplate.replace("{link}", link)

        data = {
            'subject': 'Welcome to veWriter',
            'body': html,
            'to_email': user.email
        }

        Util.send_email(data)
        return user


class UserActivateAccountSerializer(serializers.Serializer):

    def validate(self, attrs):
        try:
            uid = self.context.get("uid")
            token = self.context.get("token")

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not account_activation_token.check_token(user, token):
                raise serializers.ValidationError(
                    "Token is not valid or expired")

            user.status = 'active'
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError(
                "Token is not valid or expire")


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500)

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {"errors": {"bad_token": "Token is invalid or expired"}})


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'image']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['old_password', 'new_password']

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")

        user = self.context.get("user")

        if not check_password(old_password, user.password):
            raise serializers.ValidationError(
                "Your password was incorrect.")

        user.password_changed_at = datetime.now(tz=timezone.utc)
        user.set_password(new_password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = password_reset_token.make_token(user)
            link = f'http://localhost:3000/auth/reset-password?uid={uid}&token={token}'

            html = resetPasswordTemplate.replace("{name}", user.first_name)
            html = html.replace("{link}", link)

            data = {
                'subject': 'Reset your password',
                'body': html,
                'to_email': user.email
            }

            Util.send_email(data)

            return attrs
        raise serializers.ValidationError(
            "Account with this email doesn't exists")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password']

    def validate(self, attrs):
        try:
            password = attrs.get("password")

            uid = self.context.get("uid")
            token = self.context.get("token")

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            if not password_reset_token.check_token(user, token):
                raise serializers.ValidationError(
                    "Token is not valid or expired")

            user.password_changed_at = datetime.now(tz=timezone.utc)
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError(
                "Token is not valid or expire")
