# Generated by Django 4.0.6 on 2022-12-10 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0018_alter_announcement_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='StartDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 10, 46, 46, 88924)),
        ),
    ]