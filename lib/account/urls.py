from django.urls import path
from django.contrib.auth import views as auth_views
from account.views import LoginUser, RegisterUser, logout_user, ResetPassword, ResetPasswordConfirm

urlpatterns = [
    path('login/', LoginUser.as_view(), name="login"),
    path('registration/', RegisterUser.as_view(), name="registration"),
    path('logout/', logout_user, name="logout"),
    path('reset_password', ResetPassword.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/registration/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirm.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name="account/registration/reset_password_complete.html"), name="password_reset_complete"),
]