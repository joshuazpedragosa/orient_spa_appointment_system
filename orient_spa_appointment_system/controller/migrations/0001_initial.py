# Generated by Django 4.2.4 on 2023-09-03 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='authentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_id', models.CharField(default='', max_length=200)),
                ('priv', models.IntegerField(default=2)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('password', models.CharField(default='', max_length=200)),
                ('random_code', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'tbl_users',
            },
        ),
    ]
