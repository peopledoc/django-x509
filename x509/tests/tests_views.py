# -*- coding: utf-8 -*-

import os

from django.test import TestCase
from django.test.client import RequestFactory
from x509.django.models import Certificate
from x509.django.views import PEMFormView
from x509.exceptions import CertificateAlreadyExist

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(TEST_DIR)), "examples")


class PEMFormViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_i_can_post_a_certificate(self):
        certificat_1_path = os.path.join(TEST_EXAMPLES_DIR, 'localhost', 'client1.crt')
        with open(certificat_1_path, 'rb') as cert_file:
            request = self.factory.post('/add_pem', {'pem_file': cert_file})
            PEMFormView.as_view()(request)
        self.assertEqual(1, Certificate.objects.count())

    def test_i_cant_post_twice_the_same_certificate(self):
        certificat_1_path = os.path.join(TEST_EXAMPLES_DIR, 'localhost', 'client1.crt')
        with open(certificat_1_path, 'rb') as cert_file:
            request = self.factory.post('/add_pem', {'pem_file': cert_file})
            PEMFormView.as_view()(request)
            with self.assertRaises(CertificateAlreadyExist):
                PEMFormView.as_view()(request)
