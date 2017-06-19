# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils.timezone import now, timedelta

from ..django.models import Certificate, GenericCertificateM2M


class ModelsTestCase(TestCase):

    def test_i_can_create_a_certificate_instance(self):
        created = now()
        expire = now() + timedelta(days=320)
        test_dn = "My Distinguished Nameeeee"
        cert = Certificate.objects.create(serial='{12345678-1234-5678-1234-567812345678}',
                                          dn=test_dn,
                                          created_at=created,
                                          expire_at=expire)
        self.assertEqual(cert.created_at, created)
        self.assertEqual(cert.expire_at, expire)
        self.assertEqual(cert.dn, test_dn)

    def test_i_can_create_a_generic_certificate_m2m(self):
        cert = Certificate.objects.create(serial='{12345678-1234-5678-1234-567812345678}',
                                          dn="My Distinguished Nameeeee",
                                          created_at=now(),
                                          expire_at=now() + timedelta(days=320))
        user = User.objects.create(username="user")
        certif_link = GenericCertificateM2M.objects.create(certificate=cert,
                                                           content_type=ContentType.objects.get_for_model(User),
                                                           object_id=user.id)
        self.assertEqual(certif_link.content_object, user)
        self.assertEqual(certif_link.certificate, cert)
