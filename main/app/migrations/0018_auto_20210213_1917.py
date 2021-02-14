# Generated by Django 3.1.3 on 2021-02-13 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_profile_is_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dis_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_dislikes', to='app.VideoModels'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_likes', to='app.VideoModels'),
        ),
    ]
