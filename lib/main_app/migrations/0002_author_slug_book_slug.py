# Generated by Django 4.1.3 on 2022-11-11 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
