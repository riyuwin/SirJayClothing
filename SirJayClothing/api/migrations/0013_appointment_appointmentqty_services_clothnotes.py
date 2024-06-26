# Generated by Django 5.0.6 on 2024-05-19 11:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_services_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointmentQty',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='services',
            name='clothNotes',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
    ]
