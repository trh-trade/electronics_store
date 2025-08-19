from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.shortcuts import redirect
from django.http import HttpResponseNotFound

def redirect_to_www(request):
    host = request.get_host()
    if host == 'trh-trade.sk':
        return redirect(f"https://www.trh-trade.sk{request.get_full_path()}", permanent=True)
    # Если хост не trh-trade.sk, возвращаем 404 (или можно пропускать дальше)
    return HttpResponseNotFound("Not Found")

urlpatterns = [
    # Редирект всех запросов с корневого домена
    re_path(r'^.*$', redirect_to_www),

    # Админка
    path('admin/', admin.site.urls),

    # Основное приложение
    path('', include('main.urls')),

    # Медиа
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)