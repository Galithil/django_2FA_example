# Generated by Django 4.0.6 on 2022-08-07 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_myuser_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
    ]
