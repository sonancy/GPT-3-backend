from django.urls import path
from .views import UserLoginView, UserRegistrationView, UserActivateAccountView, UserLogoutView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, UserProfileView

urlpatterns = [
    path('auth/sign-up/', UserRegistrationView.as_view(), name='sign-up'),
    path('auth/sign-in/', UserLoginView.as_view(), name='sign-in'),
    path('auth/sign-out/', UserLogoutView.as_view(), name='sign-out'),
    path('auth/change-password/', UserChangePasswordView.as_view(),
         name='change-password'),
    path('auth/send-reset-password-email/', SendPasswordResetEmailView.as_view(),
         name='auth/send-reset-password-email'),
    path('auth/reset-password/<uid>/<token>/', UserPasswordResetView.as_view(),
         name='reset-password'),
    path('auth/activate-account/<uid>/<token>/', UserActivateAccountView.as_view(),
         name='activate-account'),

    path('users/me/', UserProfileView.as_view(), name='profile'),
]
