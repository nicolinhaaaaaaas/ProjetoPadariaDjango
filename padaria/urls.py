from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views

urlpatterns = [
    path('', views.cadastro, name='login'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('gerenciamento/', include('gerenciamento.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
