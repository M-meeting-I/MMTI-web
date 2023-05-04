# Generated by Django 4.2 on 2023-05-04 22:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('immigration', '0005_matching_profile_delete_usersurvey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='immigration/images/%Y/%m/%d/'),
        ),
    ]
