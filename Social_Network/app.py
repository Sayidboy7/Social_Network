from django.shortcuts import render, redirect
from .models import Post, History
from auth_network.models import User
from django.contrib import messages

from datetime import datetime
from django.http import JsonResponse
import json
import urllib.request

from django.utils.text import slugify
from django.http import HttpResponse
from chat.models import Conversation

import socket


# weather
API_KEY = '5747d6060ff31e78224bbf4403267468'
url = f'https://api.openweathermap.org/data/2.5/weather?q=Pitnak&units=metric&appid={API_KEY}'


def home(request):
	posts = Post.publics.all()
	user_id = None
	if 'user_id' in request.session:
		user_id = request.session['user_id']

	user = User.objects.filter(id=user_id).first()
	if user:
			request.session['subscribed'] = user.get_subscribed

	with urllib.request.urlopen(url) as response:
		raw_data = response.read()
		data = json.loads(raw_data)
    
		city_name = data.get("name")
		temp = str(data["main"]["temp"])[:2]
		condition = data["weather"][0]["description"]
		weather = f""" {city_name}: {temp}°C"""
		request.session['weather'] = weather

	context = {
		'posts' : posts,
	}
	return render(request, 'index.html', context=context)


def post_detail(request, slug):
	post = Post.objects.get(slug=slug)
	user = None
	is_anonymus = 'user_id' not in request.session
	if not is_anonymus:
		if 'user_id' in request.session:
			user_id = request.session['user_id']
			user = User.objects.get(id=user_id)
			view(user_id=user_id, post_id=post.id)

	context = {
		'post' : post,
		'liked' : json.loads(user.liked_posts) if not is_anonymus else None,
		'disliked' : request.session['disliked'] if 'disliked' in request.session else []
	}
	return render(request, 'post_detail.html', context=context)

# Profile 
def profile(request, username):
	user = User.objects.filter(username=username).first()
	if not user:
		return redirect('/')

	user_id = None
	if 'user_id' in request.session:
		user_id = request.session['user_id']

	posts = Post.objects.filter(user_id=user.id).all()
	total_views = sum([post.views for post in posts])
	total_likes = sum([post.likes for post in posts])
	current_user = User.objects.filter(id=user_id).first()

	context = {
		'user' : user,
		'total_views' : total_views,
		'total_likes' : total_likes,
		'subscribed' : current_user.get_subscribed if current_user else [],
		'current_user' : current_user
	}
	return render(request, 'profile.html', context=context)

def redirect_profile(request):
	username = None
	if 'username' in request.session:
		username = request.session['username']
	else:
		return redirect('/auth/login/')
	return redirect(f'/profile/{username}')

# viewing liking and subscribing 
def view(user_id, post_id):
	user = User.objects.get(pk=user_id)
	post = Post.objects.get(pk=post_id)

	check_history = History.objects.filter(user_id=user_id, post_id=post_id).first() 

	if check_history:
		check_history.time = datetime.now()
		check_history.save()
		return True

	post.views += 1
	history_entity = History(
		user = user,
		post = post
	)
	post.save()
	history_entity.save()

	return True


def like(request, post_slug):
	is_anonymus = True if 'user_id' not in request.session else False
	user = None
	
	if is_anonymus:
		messages.warning(request, 'Please login to like posts!')
		return redirect('post_detail', slug=post_slug)

	post = Post.objects.filter(slug=post_slug).first()
	user = User.objects.filter(id=request.session['user_id']).first()
	
	is_like = request.GET.get('like')
	is_like = 0 if is_like == 'False' else 1

	if not is_like:
		if post.id in request.session['disliked']:
			post.dislikes -= 1
			post.save()
			request.session['disliked'].remove(post.id)
			request.session.modified = True
			return redirect('post_detail', slug=post.slug)

		post.dislikes += 1
		if str(post.id) in user.liked_posts:
			post.likes -= 1
			user.liked_posts_remove(post.id)

		user.save()
		post.save()

		request.session['disliked'].append(post.id)
		request.session.modified = True
		return redirect('post_detail', slug=post.slug)

	if user.liked_posts:
		if str(post.id) in user.liked_posts:
			post.likes -= 1
			user.liked_posts_remove(post.id)
			user.save()
			post.save()
			return redirect('post_detail', slug=post.slug)
	
	user.liked_posts_add(post.id)
	post.likes += 1
	if post.id in request.session['disliked']:
		post.dislikes -= 1
		request.session['disliked'].remove(post.id)

	user.save()
	post.save()

	return redirect('post_detail', slug=post.slug)


def readed_posts(request):
	posts = []
	if 'user_id' in request.session:
		user_readed_posts = History.objects.filter(user_id=request.session['user_id']).all().order_by('-time')
		for history in user_readed_posts:
			post = Post.objects.filter(id=history.post_id).first()
			posts.append(post)

	context = {
		'posts' : posts
	}
	return render(request, 'readed_posts.html', context=context)


def lastest(request):
	posts = Post.lastest.all()
	
	context = {
		'posts' : posts
	}

	return render(request, 'lastest.html', context=context)


def post(request):
	if request.method == 'POST':
		title = request.POST.get('title').strip()
		content = request.POST.get('content').strip()

		imagefile = request.FILES.get('image') or None
		ispublic = bool(request.POST.get('ispublic'))
		tags = request.POST.get('tags')
		tags = tags.split(',')

		print(tags)
		print(type(tags))

		if not title or not content:
			messages.warning(request, message='please compelte the inputs!')
			return redirect('/post/')

		if 'user_id' not in request.session:
			messages.error(request, message='No authorizated user!')
			return redirect('/auth/login/')

		try:
			new_post = Post(
				title = title,
				content = content,
				image = imagefile,
				public = ispublic,
				user_id = request.session['user_id']
			)
			new_post.slug = slugify(new_post.title)
			new_post.save()
			new_post.tags.add(*tags)

		except:
			messages.error(request, 'Error on saving')
			return redirect('/post/')


		messages.success(request, message='Post added Successfully!')

		return redirect('/profile/')

	return render(request, 'posting.html')


def subscribe(request, ch_name):
	ch_name = ch_name.strip()
	user_id = None
	if 'user_id' in request.session:
		user_id = request.session['user_id']

	user = User.objects.filter(id=user_id).first()
	
	if not user:
		messages.warning(request, 'you need account to follow channels!')
		return redirect('/auth/login/')

	if ch_name in user.get_subscribed:
		messages.warning(request, 'you are followed already!')
		return redirect(f'/profile/{ch_name}')

	if ch_name == user.username:
		message.warning(request, 'you cant follow you own account!')
		return redirect(f'/profile/{ch_name}')

	user.add_to_subscribed(ch_name)
	user.save()

	return redirect(f'/profile/{ch_name}')


def unsubscribe(request, ch_name):
	ch_name = ch_name.strip()
	user_id = None

	if 'user_id' in request.session:
		user_id = request.session['user_id']

	user = User.objects.filter(id=user_id).first()
	
	if not user:
		messages.warning(request, 'you need account to follow channels!')
		return redirect('/auth/login/')

	if ch_name not in user.get_subscribed:
		messages.warning(request, 'you are followed already!')
		return redirect(f'/profile/{ch_name}')

	user.remove_from_subscribed(ch_name)
	user.save()

	return redirect(f'/profile/{ch_name}')


def inbox(request):
	if 'username' not in request.session:
		return redirect('/')
	user = User.objects.filter(username=request.session['username']).first()
	conversations = Conversation.objects.filter(
		participants=user).all()
	cons = {}
	for con in conversations:
		other_user = con.other_user(user.id)
		last_message = con.last_message
		cons[f'{con.id}'] = {
			'other_user' : f'{other_user.username}',
			'last_message' : f'{last_message}', 
			'created_at' : f'{con.created_at}',
			'image_url' : other_user.photo.url
		}

	context = {
		'conversations' : conversations,
		'cons' : cons
	}
	return render(request, 'chat/inbox.html', context=context)