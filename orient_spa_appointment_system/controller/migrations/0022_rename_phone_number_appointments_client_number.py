# Generated by Django 4.2.1 on 2023-10-02 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0021_rename_client_number_appointments_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointments',
            old_name='phone_number',
            new_name='client_number',
        ),
    ]