"""
URL configuration for raicescom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from core.views import translate_text, sitemap, robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # SEO URLs (outside i18n patterns)
    path('sitemap.xml', sitemap, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
]

# Add internationalization patterns
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/translate/', translate_text, name='translate_text_i18n'),
    prefix_default_language=False,  # Don't prefix the default language
)

# Add static and media files serving for both development and production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
