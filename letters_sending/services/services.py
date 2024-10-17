from authen.services import show_error


class OwnerVerificationMixin:
    """
    Миксин модификации GET и POST методов для проверки владельца объекта
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.is_superuser:
            return show_error(request, 'Доступ запрещен')

        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        if self.get_object().owner != request.user and not request.user.is_superuser:
            return show_error(request, 'Доступ запрещен')

        return super().post(request, *args, **kwargs)


class OwnerListVerificationMixin:
    """
    Миксин модификации get_queryset() на просмотр списка всех или своих объектов
    """

    list_permission = None
    list_owner_permission = None

    def get_queryset(self):

        if self.request.user.has_perm(self.list_permission):
            return super().get_queryset()
        elif self.request.user.has_perm(self.list_owner_permission):
            return super().get_queryset().filter(owner=self.request.user)
        else:
            return self.model.objects.none()
