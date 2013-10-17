======================
django-nginx-x509-auth
======================

How to enable x509 authentication with your Python WSGI app.


What do we want?
================

The aim of this project is to demonstrate how you can use Nginx to
validate a x509 certificate and allow or not the connection with your
server and with your WSGI app.


How does it works?
==================

Well, NGINX will receive the certificate, validate it and provide some headers to WSGI.
 
   - The DN of the certificate (that contains the client domain)
   - The Serial of the certificate (That is an UUID)


Nginx configuration for certificate
-----------------------------------

::

        ssl on;
        ssl_certificate /etc/ssl/www-domain.crt;
        ssl_certificate_key /etc/ssl/www-domain.key;
        ssl_client_certificate /etc/ssl/org-ca.crt;
        ssl_verify_client optional; # If the certificate is mandatory or not.


WSGI SSL verification
---------------------

::

    CERTIFICATE_IS_MANDATORY = True


    class CertificateError(Exception):
        pass


    def raise_for_certificate(self, request):
        if not CERTIFICATE_IS_MANDATORY:
            return None

        if 'HTTP_SSL_VERIFIED' in request.META and \
                request.META['HTTP_SSL_VERIFIED'] == 'SUCCESS':
            try:
                serial = UUID(request.META['HTTP_SSL_SERIAL'])
                self.certificates.get(
                    serial=str(serial).replace('-', ''))
            except Certificate.DoesNotExist:
                message = 'Access not allowed for this certificate.'
            except (ValueError, KeyError):
                message = 'Certificat serial is not a valid UUID.'
            else:
                return None
        else:
            message = 'SSL certificate invalid.'
        raise CertificateError(message)


In practice
===========

Store the certificate in Django
-------------------------------

    # -*- coding: utf-8 -*-
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from uuidfield import UUIDField
    
    
    class Certificate(models.Model):
        """Certificate x509 to contact the API."""
        site = models.ForeignKey(RH2Site)
        dn = models.TextField(_('Distinguished Name'))
        serial = UUIDField(unique=True)
        created_at = models.DateTimeField()
        expire_at = models.DateTimeField()
    
        def __unicode__(self):
            return u'%s - %s' % (self.site, self.dn)


Build the certificate
---------------------

http://suoranciata.github.io/ssl-client-auth.html