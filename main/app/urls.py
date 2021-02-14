from django.urls import path

from . import views


urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),

	path('about/', views.AboutView.as_view(), name='about'),
	path('contact/', views.ContactView.as_view(), name='contact'),

	path('valid_error/', views.ValidErrorView.as_view(), name='valid_error'),

	path('login/', views.MyProjectLoginView.as_view(), name='login_page'),
	path('register/', views.RegisterUserView.as_view(), name='register_page'),
	path('logout', views.MyProjectLogoutView.as_view(), name='logout'),

	path('fill_profile/', views.FillProfile, name='fillprofile'),
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('edit_profile/', views.EditProfile.as_view(), name='edit_profile'),
	path('update_profile/', views.UpdateProfile.as_view(), name='update_profile'),

	path('list/<int:id>/', views.ListView.as_view(), name='list'),
	path('subscribe/<int:user>/<int:id>', views.SubscribeView.as_view(), name='subscribe'),
	path('remove_subscribe/<int:user>/<int:id>', views.RemoveSubscribeView.as_view(), name='remove_subscrive'),
	path('profile/<int:id>', views.OtherProfile.as_view(), name='other_profile'),

	path('add_likes/<int:id>', views.AddLikes.as_view(), name='add_likes'),
	path('remove_likes/<int:id>', views.RemoveLikes.as_view(), name='remove_likes'),
	path('add_dis_likes/<int:id>', views.AddDisLikes.as_view(), name='add_dis_likes'),
	path('remove_dis_likes/<int:id>', views.RemoveDisLikes.as_view(), name='remove_dis_likes'),

	path('add_view/', views.VideoAddView.as_view(), name='addview'),
	path('add', views.VideoAdd.as_view(), name='add'),
	path("delete_view/<int:id>", views.VideoDelete.as_view(), name='delete_view'),

	path('review/<int:id>', views.AddReview.as_view(), name='review'),
	path('search/', views.search, name='search'),

	path("receive_email/", views.receive, name='receive_email'),
]
