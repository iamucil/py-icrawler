from django.conf import settings
from django.conf.urls import url, static

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^api/crawl/', views.Crawl, name='crawl')
]

# This is required for static files while in development mode. (DEBUG=TRUE)
# No, not releant to scrapy or crawling.
if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
