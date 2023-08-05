# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-24 11:00


import django.utils.timezone
from django.db import migrations, models

import model_utils.fields

NEW_SOURCES = {
    'Manual Enterprise Enrollment': 'manual',
    'Enterprise API Enrollment': 'enterprise_api',
    'Enterprise Enrollment URL': 'enrollment_url',
    'Enterprise Offer Redemption': 'offer_redemption',
    'Enterprise User B2C Site Enrollment': 'b2c_site',
}


def add_sources(apps, schema_editor):
    enrollment_sources = apps.get_model('enterprise', 'EnterpriseEnrollmentSource')
    for name, slug in NEW_SOURCES.items():
        enrollment_sources.objects.update_or_create(name=name, slug=slug)


def drop_sources(apps, schema_editor):
    enrollment_sources = apps.get_model('enterprise', 'EnterpriseEnrollmentSource')
    enrollment_sources.objects.filter(name__in=NEW_SOURCES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0078_auto_20191107_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterpriseEnrollmentSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now,
                    editable=False,
                    verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now,
                    editable=False,
                    verbose_name='modified')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='enterprisecourseenrollment',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='enterprise.EnterpriseEnrollmentSource'),
        ),
        migrations.AddField(
            model_name='historicalenterprisecourseenrollment',
            name='source',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                    to='enterprise.EnterpriseEnrollmentSource'),
        ),
        migrations.AddField(
            model_name='pendingenrollment',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='enterprise.EnterpriseEnrollmentSource'),
        ),
        migrations.AddField(
            model_name='historicalpendingenrollment',
            name='source',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                    to='enterprise.EnterpriseEnrollmentSource'),
        ),
        migrations.RunPython(add_sources, drop_sources)
    ]
