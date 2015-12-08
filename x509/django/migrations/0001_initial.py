# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial', models.UUIDField(unique=True)),
                ('dn', models.TextField(verbose_name=b'Distinguished Name')),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('expire_at', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenericCertificateM2M',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('certificate', models.ForeignKey(related_name='attachees', to='django.Certificate')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
