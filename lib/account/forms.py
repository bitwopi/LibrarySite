from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, UserModel, \
    _unicode_ci_compare

from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "Email"}),
    )

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Пароль"}),
    )

    error_messages = {
        "invalid_login": _(
            "Пожалуйста введите корректные email и пароль. Учтите, что "
            "поля могут быть чувствительны к регистру."
        ),
    }

    class Meta:
        fields = {"email", "password"}

    def __init__(self, request=None, *args, **kwargs):
        """
                The 'request' parameter is set for custom auth use by subclasses.
                The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                self.add_error("password", self.get_invalid_login_error())

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "Email"}),
        )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя"}),
    )
    second_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Фамилия"}),
    )
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Отчество"}),
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "Дата рождения"}),
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Подтверждение пароля"}),
    )

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "second_name", "patronymic", "birth_date"]


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': "email"}))

    def get_users(self, email):
        email_field_name = UserModel.get_email_field_name()
        users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
            }
        )
        return (
            u
            for u in users
            if u.has_usable_password()
               and _unicode_ci_compare(email, getattr(u, email_field_name))
        )


class ResetPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Новый пароль"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Подтверждение нового пароля"}))
