from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.shortcuts import redirect

# Функция редиректа с корня на www
def redirect_to_www(request):
    host = request.get_host()
    if host == 'trh-trade.sk':
        return redirect(f"https://www.trh-trade.sk{request.get_full_path()}", permanent=True)
    return None

urlpatterns = [
    # Редирект всех запросов с корневого домена (срабатывает первым)
    re_path(r'^.*$', redirect_to_www),

    # Админка Django
    path('admin/', admin.site.urls),

    # Подключение основного приложения
    path('', include('main.urls')),

    # Раздача медиа-файлов
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)