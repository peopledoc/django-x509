# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from x509.django.utils import raise_for_certificate


class WhoIsLinkedToMe(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/plain')
        response.status_code = 403

        try:
            certificate = raise_for_certificate(request.META)
        except Exception as e:
            response.write(u'%s' % e)
        else:
            response.status_code = 200
            response.write('Certificate number %d\n\n' % certificate.id)

            for attachee in certificate.attachees.all():
                response.write('Hello %s\n' % attachee.content_object)

        return response


whoami = WhoIsLinkedToMe.as_view()
