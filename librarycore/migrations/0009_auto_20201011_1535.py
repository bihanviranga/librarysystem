# Generated by Django 3.1 on 2020-10-11 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librarycore', '0008_auto_20201008_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='bookAuthor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='librarycore.author'),
        ),
    ]
