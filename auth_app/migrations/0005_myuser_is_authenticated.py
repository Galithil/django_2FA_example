# Generated by Django 4.0.6 on 2022-08-07 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_myuser_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]