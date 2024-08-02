from secrets import token_hex
from urllib.request import Request

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from authen.forms import RegisterForm, AuthForm, ProfileForm, UserPasswordResetForm, UserSetPasswordForm
from authen.models import User
from config.settings import APP_NAME, EMAIL_HOST_USER


# АВТОРИЗАЦИЯ
class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthForm

    title = "авторизация"
    extra_context = {
        'section': title,
        'header': title.title(),
        'title': title
    }


# РЕГИСТРАЦИЯ
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('authen:login')

    title = "регистрация пользователя"
    extra_context = {
        'section': 'register',
        'header': title.title(),
        'title': title
    }

    def form_valid(self, form):
        if form.is_valid():
            # создание ссылки подтверждения почты
            self.object = form.save()
            self.object.is_active = False
            self.object.token = token_hex(10)
            self.object.save()

            url = f"http://{self.request.get_host()}/user/email-confirm/{self.object.token}"
            send_mail(
                "Подтвердите свою почту",
                f"Пройдите по ссылке {url} для подтверждения регистрации на сайте {APP_NAME}",
                EMAIL_HOST_USER,
                (self.object.email,),
                fail_silently=True
            )

        return super().form_valid(form)


# ПРОФИЛЬ
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('product:list')

    title = "профиль пользователя"
    extra_context = {
        'section': 'profile',
        'header': title.title(),
        'title': title
    }

    def get_object(self, queryset=None):
        return self.request.user


# ПОДТВЕРДИТЬ ПОЧТУ
def verificate_email(request: Request, token: str) -> HttpResponse:
    """Подтвердить почту"""

    if User.objects.filter(token=token).exists():
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = None
        user.save()

        title = 'почта успешно подтверждена'
    else:
        title = 'ссылка недействительная'

    return render(
        request,
        'information.html',
        {
            'section': 'confirmation',
            'title': title,
            'header': title,
        }
    )


# СБРОС ПАРОЛЯ - ОТПРАВКА ССЫЛКИ НА ПОЧТУ
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('authen:password_reset_done')


# ВВОД НОВОГО ПАРОЛЯ
class CustomUserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('authen:password_reset_complete')

