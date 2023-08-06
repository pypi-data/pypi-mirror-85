"""
eox_tagging URL Configuration
"""
from django.conf.urls import include, url

from eox_tagging import views

urlpatterns = [
    url(r'^eox-info$', views.info_view, name='eox-info'),
    url(r'api/', include('eox_tagging.api.urls')),
]
