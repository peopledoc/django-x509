# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from uuidfield import UUIDField


class Certificate(models.Model):
    """Certificate x509 to link with something."""
    serial = UUIDField(unique=True)
    dn = models.TextField('Distinguished Name')
    created_at = models.DateTimeField(blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.dn)


class GenericCertificateM2M(models.Model):
    """Link a Certificate to any other object (User, object)."""
    certificate = models.ForeignKey(Certificate)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'%s: %s' % (self.content_object, self.certificate)
