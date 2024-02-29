from django.urls import path
from rest_framework_simplejwt.views import (
                                            TokenObtainPairView,
                                            TokenRefreshView,
                                        )
from .views import (UserRegistrationView, UserLoginView, UserProfileView, ChangePasswordView,
            SendPasswordResetEmailView, ResetPasswordView
    )





urlpatterns = [
    path('user/registration/', UserRegistrationView.as_view(), name='user_register'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/changePassword/', ChangePasswordView.as_view(), name='change_password'),
    path('user/SendPasswordResetEmail/', SendPasswordResetEmailView.as_view(), name='password_reset_email'),
    path('user/reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset-password'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]