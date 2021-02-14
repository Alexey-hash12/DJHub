from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, VideoModels, Review

class AuthUserForm(AuthenticationForm, forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')

class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('face', 'intro', 'email', 'age', 'last_name', 'first_name')


class SubscribeForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('subscribers',)


class UserVideoForm(forms.ModelForm):
	class Meta:
		model = VideoModels
		fields = ('title', 'intro', 'poster', 'video')

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('text', )				
