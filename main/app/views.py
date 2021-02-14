from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import AuthUserForm, ProfileForm, RegisterUserForm, SubscribeForm, UserVideoForm, ReviewForm
from .models import Profile, VideoModels, Review
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib import messages
# from .service import send
from .tasks import send_message
# Create your views here.

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class HomeView(ListView):
	queryset = VideoModels.objects.all().order_by('-id')
	context_object_name = 'vm'
	paginate_by = 6
	template_name = 'home.html'

	# def get_context_data(self, **kwargs):
	# 	data = super().get_context_data(**kwargs)
	# 	data['user_all'] = UserBlog.objects.all()
	# 	return data

class AddReview(View):
	def post(self, request, id):
		if request.method == 'POST':
			form = ReviewForm(request.POST)
			if form.is_valid():
				try:
					f = form.save(commit=False)
					f.auth_user = request.user
					f.parentblog_id = id
					f.save()
					return redirect('list', id)
				except ValueError:
					return render(request, 'errors/anonim_user_error.html')
			else:
				return render(request, 'errors/form_valid.html')
		else:
			return render(request, 'errors/method_allowed.html')



class ListView(View):
	def get(self, request, id):

		if cache.get(id):
			vm = cache.get(id)
			print("it is from cache")
		else:
			vm = VideoModels.objects.get(id=id)
			cache.set(id, vm)
			print("it is from db")

		rm = Review.objects.filter(parentblog=vm)

		#Neural line
		#--------------------------
		# pred = 0
		# input = [
		# 	[i for i in request.user.profile.subscribers.all()],
		# 	[j for j in request.user.profile.likes.all()],
		# 	[k for k in request.user.profile.dis_likes.all()],
		# 	[u for u in Review.objects.filter(auth_user=request.user)],
		# ]
		# print(input)

		# objects_weight = ['user', 'likes']

		# for i in input[0]:
		# 	video = VideoModels.objects.filter(user=i)


		# print(request.user.profile.likes.all())
		# print(request.user.profile.dis_likes.all())
		# print(Review.objects.filter(auth_user=request.user))



		#--------------
		return render(request, 'list.html', {'vm':vm, 'rm':rm})

class SubscribeView(View):
	def post(self, request, user, id):
		profile = Profile.objects.get(user=user)
		video = VideoModels.objects.get(id=id)
		if request.method == "POST":
			try:
				profile.subscribers.add(request.user)
				request.user.profile.subscriptions.add(profile.user)
				profile.save()
				return redirect('list', video.id)
			except:
				 return render(request, 'errors/anonimus_user.html')
		else:
			return render(request, 'errors/method_not_allowed.html')

class RemoveSubscribeView(View):
	def post(self, request, user, id):
		profile = Profile.objects.get(user=user)
		video = VideoModels.objects.get(id=id)
		if request.method == "POST":
			try:
				profile.subscribers.remove(request.user)
				request.user.profile.subscriptions.remove(profile.user)
				profile.save()
				return redirect('list', video.id)
			except:
				 return render(request, 'errors/anonimus_user.html')
		else:
			return render(request, 'errors/method_not_allowed.html')


class AddLikes(View):
	def post(self, request, id):
		video = VideoModels.objects.get(id=id)
		if request.method == 'POST':
			try:
				video.likes.add(request.user)
				request.user.profile.likes.add(video)
				video.save()
				return redirect('list', video.id)
			except:
				 return render(request, 'errors/anonimus_user.html')
		else:
			return render(request, 'errors/method_not_allowed.html')

class RemoveLikes(View):
	def post(self, request, id):
		video = VideoModels.objects.get(id=id)
		if request.method == 'POST':
			try:
				video.likes.remove(request.user)
				request.user.profile.likes.remove(video)
				video.save()
				return redirect('list', video.id)
			except ValueError:
				 return render(request, 'errors/anonimus_user.html')
		else:
			return render(request, 'errors/method_not_allowed.html')


class AddDisLikes(View):
	def post(self, request, id):
		video = VideoModels.objects.get(id=id)
		if request.method == 'POST':
			try:
				video.dis_likes.add(request.user)
				request.user.profile.dis_likes.add(video)
				video.save()
				return redirect('list', video.id)
			except:
				 return render(request, 'errors/anonimus_user.html')
		else:
			return render(request, 'errors/method_not_allowed.html')


class RemoveDisLikes(View):
	def post(self, request, id):
		video = VideoModels.objects.get(id=id)
		if request.method == 'POST':
			try:
				video.dis_likes.remove(request.user)
				request.user.profile.dis_likes.remove(video)
				video.save()
				return redirect('list', video.id)
			except ValueError:
				 return render(request, 'errors/anonimus_user.html')
		else:
			return render(request, 'errors/method_not_allowed.html')



class AboutView(View):
	def get(self, request):
		return render(request, 'about.html')

class ContactView(View):
	def get(self, request):
		return render(request, 'contact.html')


class ValidErrorView(View):
	def get(self, request):
		return render(request, 'errors/form_valid.html')

@login_required()
def FillProfile(request):
	if request.method == 'POST':
		try:
		    profile = request.user.profile
		except UserProfile.DoesNotExist:
		    profile = Profile(user=request.user)

		if request.method == 'POST':
		    form = ProfileForm(request.POST,request.FILES ,instance=profile)
		    if form.is_valid():
		        form.save()
		        return redirect('/')
		else:
		    form = ProfileForm(instance=profile)
	return render(request, 'auth/fillprofile.html')


class ProfileView(View):
	def get(self, request):
		a = request.user.profile.subscriptions.all()
		uw = VideoModels.objects.filter(user=request.user)
		return render(request, 'auth/profile.html', {'a' : a, 'uw':uw})

class OtherProfile(View):
	def get(self, request, id):
		ot = Profile.objects.get(user=id)
		vot = VideoModels.objects.filter(user=id)
		return render(request, 'auth/other_profile.html', {'ot': ot, 'vot':vot})

class VideoAddView(View):
	def get(self, request):
		context = {}
		context['form'] = UserVideoForm
		return render(request, 'video_add_view.html', context)

class VideoAdd(View):
	def post(self, request):
		if request.method == 'POST':
			form = UserVideoForm(request.POST, request.FILES)
			if form.is_valid():
				f = form.save(commit=False)
				f.user = request.user
				f.save()
				for i in request.user.profile.subscribers.all():
					if i.profile.is_newsletter and i.profile.email:
						send_message.delay(i.profile.email, request.user.username, f.title)
						return redirect('/')
		 		# return render(request, 'errors/anonumus_user.html')
			else:
				return render(request, 'errors/form_valid.html')
		else:
			return render(request, 'errors/method_not_allowed.html')

class VideoDelete(View):
	def post(self, request, id):
		if request.method == 'POST':
			f = VideoModels.objects.get(id=id).delete()
			return redirect('/')
		else:
			return render(request, 'errors/method_not_allowed.html')


class EditProfile(View):
	def get(self, request):
		profile = Profile.objects.get(user=request.user)
		return render(request, 'auth/editprofile.html', {'profile':profile})


class UpdateProfile(View):
	def post(self, request):
		profile = Profile.objects.get(user=request.user)
		if request.method == 'POST':
			f = ProfileForm(request.POST, request.FILES, instance=profile)
			if f.is_valid():
				f.save()
				return redirect('/')

			else:
				return render(request, 'errors/form_valid.html')
		else:
			return render(request, 'errors/method_not_allowed.html')


def search(request):
	a = request.GET.get('q')
	uw = VideoModels.objects.filter(title=request.GET.get('q'))
	return render(request, 'search.html', {'uw':uw, 'a':a})

def receive(request):
	p = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		if '_add' in request.POST:
			p.is_newsletter = True
			p.save()
		elif '_no' in request.POST:
			p.is_newsletter = False
			p.save()
		return redirect('/')
	else:
		return render(request, 'errors/method_not_allowed.html')

''' Auth Views '''
# Login
class MyProjectLoginView(LoginView):
	template_name = 'auth/login.html'
	form_class = AuthUserForm
	success_url = reverse_lazy('home')

	def get_success_url(self):
		return self.success_url

#logout
class MyProjectLogoutView(LogoutView):
	next_page = reverse_lazy('home')

#Registration
class RegisterUserView(CreateView):
    model = User
    template_name = 'auth/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('fillprofile')
    success_msg = 'Пользователь создан'

    def form_invalid(self, form):
	    """If the form is invalid, render the invalid form."""
	    return redirect('valid_error')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid
''''''
