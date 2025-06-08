from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('posts/', include('posts.urls')),
    path('mypage/', include('mypage.urls')),
    path('account/', include('account.urls')),
    path('chat/', include('chat.urls')),
    path('notifications/', include('notifications.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
