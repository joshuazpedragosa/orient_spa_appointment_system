# Generated by Django 4.2.4 on 2023-09-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0005_appointments_service_name_appointments_service_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='service_description',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='services',
            name='service_img',
            field=models.CharField(default='', max_length=200),
        ),
    ]
