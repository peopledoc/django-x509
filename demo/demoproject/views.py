# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from uuid import UUID

from x509.django.models import Certificate


class WhoIsLinkedToMe(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(mimetype='text/plain')
        response.status_code = 403
        if 'HTTP_SSL_CLIENT_VERIFY' not in request.META or \
                request.META['HTTP_SSL_CLIENT_VERIFY'] != 'SUCCESS':
            response.write('Missing certificate.')
            response.status_code = 403
        else:
            try:
                serial = UUID(request.META['HTTP_SSL_CLIENT_SERIAL'])
                certificate = Certificate.objects.get(
                    serial=str(serial).replace('-', ''))
            except Certificate.DoesNotExist:
                response.write('This certificate (%s) is not linked to '
                               'your app.' % serial)
            except ValueError:
                response.write('Certificat serial (%s) is not a valid UUID.' %
                               serial)
            except KeyError:
                response.write('Nginx didn\'t gave us the serial in '
                               'HTTP_SSL_CLIENT_SERIAL.')
            else:
                response.status_code = 200
                for attachee in certificate.attachees.all():
                    response.write('Hello %s\n' % attachee.content_object)

        return response


whoami = WhoIsLinkedToMe.as_view()
