# Generated by Django 4.2 on 2023-05-04 22:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('immigration', '0004_usersurvey_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matched_list', models.TextField()),
                ('last_matching_time', models.DateTimeField(auto_now=True)),
                ('ok_list', models.TextField()),
                ('final_matching', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_sex', models.BooleanField()),
                ('user_name', models.CharField(max_length=5)),
                ('user_age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('user_mbti_1', models.CharField(max_length=5)),
                ('user_mbti_2', models.CharField(max_length=5)),
                ('user_mbti_3', models.CharField(max_length=5)),
                ('user_mbti_4', models.CharField(max_length=5)),
                ('user_school', models.CharField(max_length=20)),
                ('user_image', models.ImageField(null=True, upload_to='immigration/images/%Y/%m/%d/')),
                ('user_kakaoid', models.CharField(max_length=40)),
                ('user_password', models.CharField(max_length=20)),
                ('want_age_min', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('want_age_max', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('want_mbti', models.CharField(max_length=80)),
                ('user_survey_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserSurvey',
        ),
    ]
