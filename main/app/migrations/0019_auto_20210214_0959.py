# Generated by Django 3.1.3 on 2021-02-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20210213_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_newsletter',
            field=models.BooleanField(default=None, null=True),
        ),
    ]