# -*- coding: utf-8 -*-


def get_subject_from_components(components):
    """Return the certificate subject from components list.

    >>> components = [('C', 'FR'), ('ST', 'Ile-de-France'), ('L', 'Paris'),
    ... ('O', 'Test Ltd'), ('OU', 'Test'), ('CN', 'Alain Dupont'),
    ... ('emailAddress', 'alain.dupont@localhost')]
    >>> print get_subject_from_components(components)
    /C=FR/ST=Ile-de-France/L=Paris/O=Test Ltd/OU=Test/CN=Alain \
Dupont/emailAddress=alain.dupont@localhost

    """
    return u'/' + u'/'.join(['%s=%s' % (a, b) for a, b in components])
