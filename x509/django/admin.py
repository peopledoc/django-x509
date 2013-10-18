# -*- coding: utf-8 -*-

from django.contrib import admin
from x509.django.models import Certificate, GenericCertificateM2M


class CertificateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Certificate, CertificateAdmin)


class GenericCertificateM2MAdmin(admin.ModelAdmin):
    pass


admin.site.register(GenericCertificateM2M, GenericCertificateM2MAdmin)
