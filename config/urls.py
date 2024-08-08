from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from authen.services import e_handler403
from config.settings import MEDIA_ROOT, MEDIA_URL

handler403 = e_handler403

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('user/', include('authen.urls', namespace='authen')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', include('letters_sending.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
