from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.conf import settings
from datetime import datetime
from .models import User
import jwt

SECRET_KEY = getattr(settings, 'SECRET_KEY')


class CustomMiddleware:
    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        if token:
            try:
                decode = jwt.decode(token, key=SECRET_KEY, options={"verify_signature": False},
                                    algorithms=["HS256"])

                timestamp = decode.get("iat")
                user_id = decode.get("user_id")
                user = User.objects.get(pk=user_id)
                password_changed_at = datetime.timestamp(
                    user.password_changed_at)

                if user.status == 'pending':
                    response = Response({"errors": {'non_field_error': [
                                        "Email is not verified. Please check your email inbox."]}}, status=status.HTTP_400_BAD_REQUEST)
                elif user.status == 'suspend':
                    response = Response({"errors": {'non_field_error': [
                                        "Account is not active"]}}, status=status.HTTP_400_BAD_REQUEST)
                elif (timestamp < password_changed_at):
                    response = Response({"errors": {'non_field_error': [
                                        "Credential are Invalid"]}}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    response = self.get_request(request)
                    return response
            except:
                response = Response({
                    "errors": {
                        "detail": "Given token not valid for any token type",
                        "code": "token_not_valid",
                        "messages": [
                            {
                                "token_class": "AccessToken",
                                "token_type": "access",
                                "message": "Token is invalid or expired"
                            }
                        ]
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            finally:
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
        else:
            response = self.get_request(request)
            return response
