"""
URL module for Tags API.
"""
from django.conf.urls import include, url

from eox_tagging.api.v1.routers import router

urlpatterns = [
    url(r'v1/', include(router.urls)),
]
