# Generated by Django 3.1 on 2020-08-26 06:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('librarycore', '0002_bookinstance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='id',
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='instanceSerialNum',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
