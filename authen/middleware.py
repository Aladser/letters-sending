from django.core.cache import cache
from django.urls import reverse


class ClearCacheOnLogoutMiddleware:
    def process_response(self, request, response):
        if request.path == reverse('authen:logout'):
            cache.clear()

        return response
