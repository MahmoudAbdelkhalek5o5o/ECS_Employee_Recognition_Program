# Generated by Django 4.0.6 on 2022-11-05 17:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_announcement_enddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='StartDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 5, 19, 49, 32, 134310)),
        ),
    ]