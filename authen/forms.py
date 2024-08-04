from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from authen.models import User
from libs.custom_formatter import CustomFormatter


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomFormatter.format_form_fields(self)

    class Meta:
        model = User
        fields = '__all__'


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomFormatter.format_form_fields(self)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class ProfileForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomFormatter.format_form_fields(self)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Электронная почта",
        max_length=254,
        widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'введите email',
            "autocomplete": "email"}
        )
    )


class UserSetPasswordForm(SetPasswordForm):
    error_messages = {"password_mismatch": "Пароли не совпадают"}
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите новый пароль',
                "autocomplete": "new-password"
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Подтвердите новый пароль',
                "autocomplete": "new-password"}
        ),
    )
