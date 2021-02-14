from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class VideoModels(models.Model):
	views = models.IntegerField(default=0)
	title = models.CharField(max_length=150)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	intro = models.TextField()
	poster = models.ImageField(upload_to='images/', null=True)
	video = models.FileField(upload_to='video/', null=True)
	date = models.DateTimeField(auto_now=True)
	likes = models.ManyToManyField(User, related_name='likes')
	dis_likes = models.ManyToManyField(User, related_name='dis_likes')

	def __str__(self):
		return self.title

class Profile(models.Model):
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	face = models.ImageField(upload_to='user_faces/', null=True, blank=True)
	intro = models.TextField(null=True)
	email = models.EmailField(null=True, blank=True)
	age = models.IntegerField(default=18, null=True, blank=True)
	subscribers = models.ManyToManyField(User, default=0, related_name='subscribers', blank=True)
	subscriptions = models.ManyToManyField(User, default=0, related_name='subscriptions', blank=True)
	likes = models.ManyToManyField(VideoModels, related_name='user_likes', blank=True, null=True)
	dis_likes = models.ManyToManyField(VideoModels, related_name='user_dislikes', blank=True,null=True)
	is_newsletter = models.BooleanField(null=True)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Review(models.Model):
	auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	text = models.TextField()
	parentblog = models.ForeignKey(VideoModels, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now=True, null=True)
	parentreview = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	isparent = models.BooleanField(null=True, blank=True)

	def __str__(self):
		return f"{self.auth_user}: {self.parentblog} ({self.parentblog.id}) :: {self.parentblog}"
