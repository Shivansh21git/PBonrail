from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # PWA: Serve manifest.json
    path('manifest.json', serve, {
        'document_root': settings.STATIC_ROOT,
        'path': 'core/manifest.json'
    }),

    # PWA: Serve service-worker.js
    path('service-worker.js', serve, {
        'document_root': settings.STATIC_ROOT,
        'path': 'service-worker.js'
    }),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
