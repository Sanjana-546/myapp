"""
URL configuration for myapp project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

from blog.admin import admin_site

urlpatterns = [
    path('', RedirectView.as_view(url='/blog/', permanent=False)),
    path('blog', RedirectView.as_view(url='/blog/', permanent=False)),
    path('blog/', include('blog.urls')),
    path('admin/', admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
