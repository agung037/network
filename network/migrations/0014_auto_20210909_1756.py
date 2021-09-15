# Generated by Django 3.2.3 on 2021-09-09 17:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20210909_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followers',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='set_followings', to=settings.AUTH_USER_MODEL),
        ),
    ]