# -*- coding: utf-8 -*-

import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from x509.django.forms import PEMForm
from x509.exceptions import CertificateAlreadyExist

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(TEST_DIR)), "examples")


class CertificateFormTestCase(TestCase):

    def test_when_i_post_empty_form_it_is_a_fail(self):
        form = PEMForm(data={})
        self.assertFalse(form.is_valid())

    def test_when_i_post_a_good_form_it_is_valid(self):
        certificat_1_path = os.path.join(TEST_EXAMPLES_DIR, 'localhost', 'client1.crt')

        with open(certificat_1_path, 'rb') as cert_file:
            form = PEMForm(data={}, files={'pem_file': SimpleUploadedFile('pem_file', cert_file.read())})
            self.assertTrue(form.is_valid())

    def test_when_i_post_a_good_form_once_i_got_a_certificate(self):
        certificat_1_path = os.path.join(TEST_EXAMPLES_DIR, 'localhost', 'client1.crt')

        with open(certificat_1_path, 'rb') as cert_file:
            form = PEMForm(data={}, files={'pem_file': SimpleUploadedFile('pem_file', cert_file.read())})
            form.is_valid()
            certificate = form.get_certificate()
            self.assertEqual(certificate.serial, "34fed2e8613747cb904f935dc17f1aba")

    def test_when_i_post_a_good_form_twice_i_got_an_exception(self):
        certificat_1_path = os.path.join(TEST_EXAMPLES_DIR, 'localhost', 'client1.crt')

        with open(certificat_1_path, 'rb') as cert_file:
            form = PEMForm(data={}, files={'pem_file': SimpleUploadedFile('pem_file', cert_file.read())})
            form.is_valid()
            form.get_certificate()

        with open(certificat_1_path, 'rb') as cert_file:
            form = PEMForm(data={}, files={'pem_file': SimpleUploadedFile('pem_file', cert_file.read())})
            form.is_valid()
            with self.assertRaises(CertificateAlreadyExist):
                form.get_certificate()
