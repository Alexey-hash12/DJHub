# Generated by Django 3.1.3 on 2021-02-11 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20210203_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodels',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
