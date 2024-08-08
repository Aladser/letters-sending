from authen.services import show_error


class OwnerVerificationMixin:
    """ Модификации GET и POST методов для проверки владельца объекта """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.is_superuser:
            return show_error(request, 'Доступ запрещен')

        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        if self.get_object().owner != request.user and not request.user.is_superuser:
            return show_error(request, 'Доступ запрещен')

        return super().post(request, *args, **kwargs)
