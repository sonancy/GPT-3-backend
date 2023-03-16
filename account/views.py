from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, UserLogoutSerializer, UserActivateAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


class UserRegistrationView(APIView):

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "Email verify link send to your email. Please check your email inbox."}, status=status.HTTP_201_CREATED)


class UserActivateAccountView(APIView):

    def post(self, request, uid, token, format=None):
        serializer = UserActivateAccountSerializer(
            data=request.data, context={"uid": uid, "token": token})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)


class UserLoginView(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.status == 'pending':
                return Response({"errors": {'non_field_error': ["Email is not verified. Please check your email inbox."]}}, status=status.HTTP_400_BAD_REQUEST)
            elif user.status == 'suspend':
                return Response({"errors": {'non_field_error': ["Account is not active"]}}, status=status.HTTP_400_BAD_REQUEST)
            else:
                token = get_tokens_for_user(user=user)
                return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": {'non_field_error': ["Credential are Invalid"]}}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Signed out successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):

    def post(self, request, format=None):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        if user.status == 'pending':
            return Response({"errors": {'non_field_error': ["Email is not verified. Please check your email inbox."]}}, status=status.HTTP_400_BAD_REQUEST)
        elif user.status == 'suspend':
            return Response({"errors": {'non_field_error': ["Account is not active"]}}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password reset link send to your email. Please check your email inbox."}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
