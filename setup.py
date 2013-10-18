# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os.path import abspath, dirname, join
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, whose path is supposed relative
    to this module."""
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


if __name__ == '__main__':  # ``import setup`` doesn't trigger setup().
    setup(
        name='django-x509',
        version=read_relative_file('VERSION').strip(),
        description="Let you be behind a nginx configuration an get "
                    "x509 auth credentials",
        long_description=read_relative_file('README.rst'),
        classifiers=['Development Status :: 4 - Beta',
                     'Environment :: Web Environment',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3'],
        keywords='django wsgi x509 auth',
        author='Rémy Hubscher',
        author_email='hubscher.remy@gmail.com',
        url='https://github.com/novapost/django-x509',
        license='MIT Licence',
        packages=['x509'],
        include_package_data=True,
        zip_safe=False,
        install_requires=['setuptools>=1.1.6', 'flask'],
        entry_points={
            'console_scripts': [
                'test_app = x509.test_app:main',
            ]
        }
    )
