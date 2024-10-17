from django.shortcuts import render

from config.settings import CACHED_ENABLED
from libs.managed_cache import ManagedCache


class ManagedCacheMixin:
    """
        Миксин управляемоего кэша
        Заменяет get-,render_to_response-методы CBV-контроллера
    """

    cached_key = None
    __exception_message = 'Не установлен ключ "cached_key" класса CachedStreamMixin'

    def get(self, *args, **kwargs):
        if not CACHED_ENABLED:
            return super().get(*args, **kwargs)

        if self.cached_key is None:
            raise Exception(self.__exception_message)

        # если кэшируется страница объекта
        if 'pk' in kwargs:
            self.cached_key += '_' + str(kwargs['pk'])

        cached_data = ManagedCache.get_data(self.cached_key, self.request.user.pk)
        if cached_data is not None:
            return cached_data

        return super().get(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if not CACHED_ENABLED:
            return super().render_to_response(context, **response_kwargs)

        if self.cached_key is None:
            raise Exception(self.__exception_message)

        response = render(self.request, self.template_name, context)
        ManagedCache.save_data(self.cached_key, self.request.user.pk, response)
        return response
