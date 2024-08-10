from secrets import token_hex
from urllib.request import Request

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from authen.forms import RegisterForm, AuthForm, ProfileForm, UserPasswordResetForm, UserSetPasswordForm
from authen.models import User
from authen.services import CustomLoginRequiredMixin, show_error
from config.settings import APP_NAME, EMAIL_HOST_USER


# АВТОРИЗАЦИЯ
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthForm

    title = "авторизация"
    extra_context = {
        'header': title.title(),
        'title': title
    }


# ВЫХОД ИЗ СИСТЕМЫ
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


# РЕГИСТРАЦИЯ
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('authen:login')

    title = "регистрация пользователя"
    extra_context = {
        'header': title.title(),
        'title': title
    }

    def form_valid(self, form):
        if form.is_valid():
            # создание ссылки подтверждения почты
            users_group = Group.objects.get(name='user')
            self.object = form.save()
            self.object.is_active = False
            self.object.token = token_hex(10)
            self.object.groups.add(users_group)
            self.object.save()

            url = f"http://{self.request.get_host()}/user/email-confirm/{self.object.token}"
            send_mail(
                "Подтвердите свою почту",
                f"Пройдите по ссылке {url} для подтверждения регистрации на сайте {APP_NAME}",
                EMAIL_HOST_USER,
                (self.object.email,),
                fail_silently=True
            )
            header = 'Регистрация успешно завершена!'
            description = 'Ссылка для подтверждения регистрации отправлена на вашу почту.'
            return render(self.request, 'info.html', {'header': header, 'description': description})

        return super().form_valid(form)


# ПРОФИЛЬ
class ProfileView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('letter_sending_list')

    title = "Профиль пользователя"
    extra_context = {
        'header': title,
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
        'info.html',
        {
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


# СПИСОК ПОЛЬЗОВАТЕЛЕЙ
class UserListView(CustomLoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'authen.view_user'

    model = User
    template_name = "user/list.html"
    title = 'список пользователей'
    extra_context = {
        'title': title,
        'header': title.capitalize()
    }


# УСТАНОВИТЬ АКТИВНОСТЬ ПОЛЬЗОВАТЕЛЯ
@login_required
@permission_required('authen.block_user')
def set_user_activation(request):
    """установить активность пользователя """

    user = User.objects.filter(pk=request.POST['pk'])
    if user.exists():
        user = user.first()

        # попытка активации пользователя менеджером
        if not request.user.is_superuser and not user.is_active:
            return show_error(request, 'Недостаточно права для активации пользователя')
        # попытка заблокировать самого себя
        if request.user == user:
            return show_error(request, 'Вы пытаетесь заблокировать самого себя')
        # попытка заблокировать суперпользователя несуперпользователем
        if user.is_superuser and user.is_active and not request.user.is_superuser:
            return show_error(request, 'Нельзя заблокировать суперпользователя')

        user.is_active = not user.is_active
        user.save()
        return redirect(reverse_lazy('authen:index'))
    else:
        return show_error(request, f'Пользователь с почтой {request.POST['email']} не найден')
