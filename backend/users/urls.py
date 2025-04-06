from django.urls import path
from .views import (
    RegisterAdminView, RegisterUserView, CompleteRegistrationView,
    GetUserProfileView, GetUserByTokenView, VerifyAdminView,
    LoginView, UpdateProfileView, ForgotPasswordView, ResetPasswordView,
    LogoutView, UserListView, UserDetailView, UserStatsView
)

urlpatterns = [
    path('register/admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('register/user/', RegisterUserView.as_view(), name='register-user'),
    path('complete-registration/', CompleteRegistrationView.as_view(), name='complete-registration'),
    path('profile/', GetUserProfileView.as_view(), name='user-profile'),
    path('user-by-token/', GetUserByTokenView.as_view(), name='user-by-token'),
    path('verify-admin/', VerifyAdminView.as_view(), name='verify-admin'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/stats/', UserStatsView.as_view(), name='user-stats'), 

]
