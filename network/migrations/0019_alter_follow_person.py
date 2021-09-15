# Generated by Django 3.2.3 on 2021-09-11 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_alter_follow_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='the_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
