# Generated by Django 4.1.4 on 2024-05-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_servicesoffered_services_clothoffered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]