from django.conf.urls import patterns, url, include
from django.contrib import admin

from x509.django.views import pem_form_view
from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.whoami, name='whoami'),
    url(r'^add_pem/$', pem_form_view, name='whoami'),
    url(r'^admin/', include(admin.site.urls)),

)
