from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('reports/', include('reports.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
admin.site.site_title = "Hotel Management Dashboard"
admin.site.site_header = "Hotel Management Admin"
admin.site.index_title = "Hotel Management Admin"