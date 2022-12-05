# Generated by Django 4.0.6 on 2022-12-04 13:37

import Rewards.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rewards', '0014_alter_redemption_request_approved_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='accepts_direct',
        ),
        migrations.AlterField(
            model_name='redemption_request',
            name='approved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 4, 15, 37, 27, 817620), null=True),
        ),
        migrations.AlterField(
            model_name='reward',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 4, 15, 37, 27, 816621), validators=[Rewards.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 4, 15, 37, 27, 815624), validators=[Rewards.models.validate_year]),
        ),
    ]