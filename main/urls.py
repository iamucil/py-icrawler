from django.conf import settings
from django.conf.urls import url, static
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='main/index.html'), name='home'),
    url(r'^api/crawl/', views.Crawl, name='crawl')
]

# This is required for static files while in development mode. (DEBUG=TRUE)
# No, not releant to scrapy or crawling.
if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
