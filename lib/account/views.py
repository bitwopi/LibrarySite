import os
import mimetypes

from django.shortcuts import redirect
from django.http import FileResponse, StreamingHttpResponse
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from wsgiref.util import FileWrapper

from account.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordConfirmForm
from main_app.models import Rent
from main_app.utils import get_month_report


class LoginUser(LoginView):
    template_name = 'account/registration/login_form.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context


class RegisterUser(CreateView):
    template_name = 'account/registration/registration_form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context


class ResetPassword(auth_views.PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'account/registration/reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super(ResetPassword, self).get_context_data(**kwargs)
        context['title'] = "Введите свой email для смены пароля"
        return context


class ResetPasswordConfirm(auth_views.PasswordResetConfirmView):
    form_class = ResetPasswordConfirmForm
    template_name = 'account/registration/reset_form.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordConfirm, self).get_context_data(**kwargs)
        context['title'] = "Восстановление пароля"
        return context


class Profile(TemplateView):
    template_name = 'account/profile/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['rents'] = Rent.objects.filter(user_email=self.request.user.email)
        context['title'] = "Профиль"
        if self.request.user.group.name == 'accountant':
            context['report_url'] = get_month_report()
        return context


def logout_user(request):
    logout(request)
    return redirect('home')


def download_report(request):
    if request.user.group.name == 'accountant':
        the_file = get_month_report()
        filename = os.path.basename(the_file)
        response = StreamingHttpResponse(
            FileWrapper(
                open(the_file, "rb"),
            ),
            content_type=mimetypes.guess_type(the_file)[0],
        )
        response["Content-Length"] = os.path.getsize(the_file)
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
