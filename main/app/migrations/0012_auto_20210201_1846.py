# Generated by Django 3.1.3 on 2021-02-01 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210201_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dis_likes',
            field=models.ManyToManyField(related_name='user_dislikes', to='app.VideoModels'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(related_name='user_likes', to='app.VideoModels'),
        ),
    ]