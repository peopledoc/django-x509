# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.db import models
from x509.django.compat import UUIDField

try:
    from django.contrib.contenttypes.generic import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.fields import GenericForeignKey


class Certificate(models.Model):
    """Certificate x509 to link with something."""
    serial = UUIDField(unique=True)
    dn = models.TextField('Distinguished Name')
    created_at = models.DateTimeField(blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.dn


class GenericCertificateM2M(models.Model):
    """Link a Certificate to any other object (User, object)."""
    certificate = models.ForeignKey(Certificate, related_name='attachees')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'%s: %s' % (self.content_object, self.certificate)
