# Generated by Django 5.0.6 on 2024-05-18 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_productname_services_servicesoffered_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='servicesOffered',
            new_name='clothOffered',
        ),
        migrations.RenameField(
            model_name='services',
            old_name='servicesPrice',
            new_name='clothPrice',
        ),
        migrations.RenameField(
            model_name='services',
            old_name='servicesSize',
            new_name='clothSize',
        ),
        migrations.RenameField(
            model_name='services',
            old_name='servicesSchool',
            new_name='clothforSchool',
        ),
    ]
