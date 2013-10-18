# -*- coding: utf-8 -*-
from uuid import UUID
from x509.django.models import Certificate
from x509.exceptions import CertificateMissing, CertificateInvalid


def raise_for_certificate(environ):
    if 'HTTP_SSL_CLIENT_VERIFY' not in environ or \
            environ['HTTP_SSL_CLIENT_VERIFY'] != 'SUCCESS':
        raise CertificateMissing()
    else:
        try:
            serial = UUID(environ['HTTP_SSL_CLIENT_SERIAL'])
            certificate = Certificate.objects.get(
                serial=str(serial).replace('-', ''))
        except Certificate.DoesNotExist:
            CertificateInvalid('This certificate (%s) is not linked to '
                               'your app.' % serial)
        except ValueError:
            CertificateInvalid('Certificat serial (%s) is not a valid UUID.' %
                               serial)
        except KeyError:
            raise KeyError('Nginx didn\'t gave us the serial in '
                           'HTTP_SSL_CLIENT_SERIAL.')
        else:
            return certificate
