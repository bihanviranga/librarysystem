# Generated by Django 3.1 on 2020-09-12 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('librarycore', '0005_auto_20200910_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='borrowedBy',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrowedBook', to=settings.AUTH_USER_MODEL),
        ),
    ]
