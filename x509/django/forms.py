# -*- coding: utf-8 -*-
from OpenSSL import crypto
from cStringIO import StringIO
from dateutil.parser import parse
from uuid import UUID

from django import forms

from x509.exceptions import CertificateAlreadyExist
from x509.utils import get_subject_from_components
from x509.django.models import Certificate


class PEMForm(forms.Form):
    pem_file = forms.FileField()

    def get_certificate(self):
        # Get the file in a StringIO
        f = StringIO()
        for chunk in self.cleaned_data['pem_file'].chunks():
            f.write(chunk)

        # Read Certificate Informations
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.getvalue())

        params = {}
        serial = UUID(str(hex(
            cert.get_serial_number())).lstrip('0x').rstrip('L'))
        params['serial'] = str(serial).replace('-', '')
        params['dn'] = get_subject_from_components(
            cert.get_subject().get_components())
        params['created_at'] = parse(cert.get_notBefore())
        params['expire_at'] = parse(cert.get_notAfter())

        try:
            certificate = Certificate.objects.get(serial=params['serial'])
        except Certificate.DoesNotExist:
            return Certificate.objects.create(**params)
        else:
            exception = CertificateAlreadyExist(
                'This certificate already exists %s' % params['serial'])
            exception.certificate = certificate
            raise exception
