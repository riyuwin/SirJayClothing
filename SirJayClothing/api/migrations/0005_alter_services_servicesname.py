# Generated by Django 5.0.6 on 2024-05-14 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='servicesName',
            field=models.CharField(max_length=500),
        ),
    ]
