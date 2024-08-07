from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Кастомизированный миксин обязательной авторизации"""

    login_url = reverse_lazy('authen:login')
    redirect_field_name = 'redirect_to'


def e_handler403(request, exception = None):
    """верстка ошибки 403"""

    return render(request,
                  'info.html',
                  status=403,
                  context={'title':'Доступ запрещен', 'description':f'Доступ запрещен\n {exception}'})
