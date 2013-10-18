from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

)
