# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.http import HttpResponse

from x509.django.forms import PEMForm


class PEMFormView(FormView):
    form_class = PEMForm
    template_name = 'x509/pem_form.html'

    def form_valid(self, form):
        certificate = form.get_certificate()
        print certificate
        return HttpResponse('%s as been imported.'
                            '<a href=".">Add another one</a>.' % certificate)


pem_form_view = PEMFormView.as_view()
