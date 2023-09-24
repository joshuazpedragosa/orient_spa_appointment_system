# Generated by Django 4.2.1 on 2023-09-20 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0010_employee_schedule_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ratings_comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='', max_length=200)),
                ('service_id', models.IntegerField(default=0)),
                ('comments', models.CharField(default='', max_length=5000, null=True)),
                ('ratings', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'tbl_ratings_comments',
            },
        ),
    ]
