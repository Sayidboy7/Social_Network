from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from datetime import datetime

from django.db.models import Q


def login(user):
	try:
		user = True
		user.last_login = datetime.utcnow()
		user.save()
	except:
		return False

	return True


def create_user(data):
	user = User(
		username = data['username'],
		firstname = data['firstname'],
		lastname = data['lastname'],
		email = data['email'],
		password = data['password1']
	)

	user.save()


def login_clearly(request):
	if request.method == 'POST':
		username = request.POST.get('username').strip()
		password = request.POST.get('password').strip()

		if not username or not password:
			messages.warning(request, message='username or password is empty! Please fill the forms correct.')
			return redirect('/auth/login/')

		user = User.objects.filter(Q(username=username) | Q(email=username)).first()

		if not user:
			messages.error(request, message='user not exists!')
			return redirect('/auth/login/')

		if user.password == password:
			login(user)
			request.session['username'] = user.username
			request.session['user_id'] = user.id
			request.session['active'] = True
			request.session['disliked'] = []
			user.last_login = datetime.now()

			messages.success(request, message='Successfully login!')
			return redirect('/')
		else:
			messages.error(request, message='Username or password is incorrect!')
			return redirect('/auth/login/')

	return render(request, 'auth/login.html')


def register(request):
	if request.method == 'POST':
		firstname = request.POST.get('firstname').strip()
		lastname = request.POST.get('lastname').strip()
		username = request.POST.get('username').strip()
		email = request.POST.get('email').strip()
		age = request.POST.get('age') # optional
		password1 = request.POST.get('password1').strip()
		password2 = request.POST.get('password2').strip()


		if not firstname or not lastname or not username:
			messages.warning(request, message='please complete the forms correctly!')
			
			return redirect('/auth/register/')

		if len(firstname) < 2 or len(lastname) < 2:
			messages.warning(request, message='Firstname and Lastname should be more than 2 charecters!')

			return redirect('/auth/register/')

		check_username = User.objects.filter(username=username).first()

		if check_username:
			messages.warning(request, message='Username already taken')
			return redirect('/auth/register/')

		if not email:
			messages.warning(request, message='Email is required please type in !')
			return redirect('/auth/register/')

		if '@' not in email:
			messages.warning(request, message='Email format is incorrect!')
			return redirect('/auth/register/')

		if password1 != password2:
			messages.warning(request, message='Paswords didn\'t match! please type correctly !')
			return redirect('/auth/register/')

		create_user(request.POST)
		return redirect('/auth/login/')

	return render(request, 'auth/register.html')

def logout(request):
	if 'username' in request.session or 'user_id' in request.session:
		try:
			user = User.objects.filter(Q(username=request.session['username']) | Q(id=request.session['user_id'])).first()
			user.active = False
			user.last_logout = datetime.now()
			user.save()
		except:
			messages.error(request, message='Logout error!')


		
		request.session.flush()
		

		messages.success(request, message='Logged Out!')
		return redirect('/')
	else:
		return redirect('/auth/login')

