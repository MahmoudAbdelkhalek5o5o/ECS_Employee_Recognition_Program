# Generated by Django 4.0.6 on 2022-11-22 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_announcement_title_alter_announcement_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='StartDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 22, 16, 30, 48, 675846)),
        ),
    ]