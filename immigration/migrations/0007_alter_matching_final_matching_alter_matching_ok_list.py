# Generated by Django 4.2 on 2023-05-05 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immigration', '0006_alter_profile_user_alter_profile_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matching',
            name='final_matching',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='matching',
            name='ok_list',
            field=models.TextField(null=True),
        ),
    ]