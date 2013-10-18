===========
django-x509
===========

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

    upstream app_server {
        # For a TCP configuration:
        server 127.0.0.1:8000 fail_timeout=0;
    }
    
    
    server {
        listen 443 default;
    
        location / {
            try_files $uri @proxy_to_app;
        }
    
        # Proxy to frontend application (WSGI).
        location @proxy_to_app {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto 'https';
            proxy_set_header Host $http_host;

            # Set to header x509 credentials
            proxy_set_header SSL-client-serial $ssl_client_serial;
            proxy_set_header SSL-client-dn $ssl_client_s_dn;
            proxy_set_header SSL-client-verify $ssl_client_verify;

            proxy_redirect off;
            proxy_pass http://app_server;
        }
    
            ssl on;
            ssl_certificate /etc/ssl/www-domain.crt;
            ssl_certificate_key /etc/ssl/www-domain.key;
            ssl_client_certificate /etc/ssl/org-ca.crt;
            ssl_verify_client optional;  # on | off | optional | optional_no_ca
    
            ssl_protocols       SSLv3 TLSv1 TLSv1.1 TLSv1.2;
            ssl_ciphers         HIGH:!RC4:!DES!3DES:!RC2:!MD5:!EXP:!aNULL:!eNULL;
    }


Test your configuration
-----------------------

::

    $ python test_app.py
     * Running on http://127.0.0.1:8000/
     * Restarting with reloader

Then using curl::

    curl -k 'https://localhost' --key examples/localhost/client.key --cert examples/localhost/client.crt 

    {'CONTENT_LENGTH': '',
     'CONTENT_TYPE': '',
     'HTTP_ACCEPT': '*/*',
     'HTTP_CONNECTION': 'close',
     'HTTP_HOST': 'localhost',
     'HTTP_SSL_CLIENT_DN': '/C=FR/ST=Ile-de-France/L=Paris/O=Test Ltd/OU=Test/CN=Alain Dupont/emailAddress=alain.dupont@localhost',
     'HTTP_SSL_CLIENT_SERIAL': 'CA92CBE98DDD421A9E4263254E413017',
     'HTTP_SSL_CLIENT_VERIFY': 'SUCCESS',
     'HTTP_USER_AGENT': 'curl/7.32.0',
     'HTTP_X_FORWARDED_FOR': '127.0.0.1',
     'HTTP_X_FORWARDED_PROTO': 'https',
     'PATH_INFO': '/',
     'QUERY_STRING': '',
     'REMOTE_ADDR': '127.0.0.1',
     'REMOTE_PORT': 51923,
     'REQUEST_METHOD': 'GET',
     'SCRIPT_NAME': '',
     'SERVER_NAME': '127.0.0.1',
     'SERVER_PORT': '8000',
     'SERVER_PROTOCOL': 'HTTP/1.0',
     'SERVER_SOFTWARE': 'Werkzeug/0.9.4',
     'werkzeug.request': <Request 'http://localhost/' [GET]>,
     'werkzeug.server.shutdown': <function shutdown_server at 0xb6d6eb1c>,
     'wsgi.errors': <open file '<stderr>', mode 'w' at 0xb75250d0>,
     'wsgi.input': <socket._fileobject object at 0xb6d698ec>,
     'wsgi.multiprocess': False,
     'wsgi.multithread': False,
     'wsgi.run_once': False,
     'wsgi.url_scheme': 'http',
     'wsgi.version': (1, 0)}

.. Note:: If you get a certificate error, you may not be using the CA that signed the client_certificate.    


WSGI SSL verification
---------------------

::

    CERTIFICATE_IS_MANDATORY = True


    class CertificateError(Exception):
        pass


    def raise_for_certificate(self, environ):
        if not CERTIFICATE_IS_MANDATORY:
            return None

        if 'HTTP_SSL_VERIFIED' in environ and \
                environ['HTTP_SSL_CLIENT_VERIFIED'] == 'SUCCESS':
            try:
                serial = UUID(environ['HTTP_SSL_CLIENT_SERIAL'])
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

::

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

::

    # Create the CA Key and Certificate for signing Client Certs
    openssl req -new -x509 -days 3650 -newkey rsa:4096 -out client.crt -keyout ca.key

    # Create the Server Key, CSR, and Certificate
    openssl req -new -newkey rsa:4096 -nodes -out server.csr -keyout server.key

    # We're self signing our own server cert here.  This is a no-no in production.
    openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
    
    # Create the Client Key and CSR
    openssl req -new -newkey rsa:4096 -out client.csr -keyout client.key
    
    # Sign the client certificate with our CA cert.  Unlike signing our own server cert, this is what we want to do.
    serial="0x`python -c "import uuid; print(str(uuid.uuid4()).replace('-', ''))"`"
    openssl x509 -req -days 3650 -in client.csr -CA ca.crt -CAkey ca.key -set_serial "${serial}" -out client.crt

    # Verify the client certificate
    openssl x509 -subject -serial -noout -in client.crt
    
    # Or
    openssl x509 -text -noout -in client.crt
