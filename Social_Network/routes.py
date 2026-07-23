from django.urls import path
from .app import *

urlpatterns = [
	path('', home, name='index'),
	path('post/detail/<slug>', post_detail, name='post_detail'),
	path('profile/<username>', profile, name='profile'),
	path('profile/', redirect_profile, name='redirect_profile'),

	# social interactions
	path('like/<post_slug>', like, name='like'),
	path('readed_posts/', readed_posts, name='readed_posts'),
	path('lastest/', lastest, name='lastest'),
	path('subscribe/<ch_name>', subscribe, name='subscribe'),
	path('unsubscribe/<ch_name>', unsubscribe, name='unsubscribe'),

	# adding editing
	path('post/', post, name='post'),
]
