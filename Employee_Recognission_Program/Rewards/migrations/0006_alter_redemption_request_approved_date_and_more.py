# Generated by Django 4.0.6 on 2022-12-13 09:03

import Rewards.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rewards', '0005_alter_redemption_request_approved_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redemption_request',
            name='approved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 11, 3, 18, 427751), editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='reward',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 11, 3, 18, 426754), validators=[Rewards.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 11, 3, 18, 426754), validators=[Rewards.models.validate_year]),
        ),
    ]
