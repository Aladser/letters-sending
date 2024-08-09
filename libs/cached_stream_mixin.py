from django.shortcuts import render

from config.settings import CACHED_ENABLED
from libs.cached_stream import CachedStream


class CachedStreamMixin:
    """Миксин кэширования страницы контроллера"""

    cached_key = None
    __exception_message = 'Не установлен ключ cached_key класса CachedStreamMixin'

    def get(self, *args, **kwargs):
        if self.cached_key is None:
            raise Exception(self.__exception_message)

        if CACHED_ENABLED:
            cached_data = CachedStream.get_data(self.cached_key, self.request.user.pk)
            if cached_data is not None:
                return cached_data

        return super().get(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.cached_key is None:
            raise Exception(self.__exception_message)

        response = render(self.request, self.template_name, context)
        if CACHED_ENABLED:
            CachedStream.save_data(self.cached_key, self.request.user.pk, response)
        return response
