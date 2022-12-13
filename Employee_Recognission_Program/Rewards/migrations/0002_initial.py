<<<<<<< Updated upstream
# Generated by Django 4.1 on 2022-11-26 14:06
=======
# Generated by Django 4.1 on 2022-12-11 11:41
>>>>>>> Stashed changes

import Rewards.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Rewards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reward',
            name='creator',
<<<<<<< Updated upstream
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reward_creator', to=settings.AUTH_USER_MODEL),
=======
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reward_creator', to=settings.AUTH_USER_MODEL),
>>>>>>> Stashed changes
        ),
        migrations.AddField(
            model_name='reward',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rewards.vendor'),
        ),
        migrations.AddField(
            model_name='redemption_request',
            name='approved_by',
<<<<<<< Updated upstream
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL),
=======
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL),
>>>>>>> Stashed changes
        ),
        migrations.AddField(
            model_name='redemption_request',
            name='employee',
<<<<<<< Updated upstream
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL, validators=[Rewards.models.validate_admin]),
=======
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL, validators=[Rewards.models.validate_admin]),
>>>>>>> Stashed changes
        ),
        migrations.AddField(
            model_name='redemption_request',
            name='voucher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rewards.reward'),
        ),
        migrations.AddField(
            model_name='budget',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
