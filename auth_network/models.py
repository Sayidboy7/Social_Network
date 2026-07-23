from django.db import models
import json

class User(models.Model):
	username = models.CharField(max_length=250, unique=True)
	firstname = models.CharField(max_length=250)
	lastname = models.CharField(max_length=200)
	age = models.IntegerField(null=True, blank=True)
	email = models.CharField(max_length=200, unique=True)
	photo = models.ImageField(upload_to='static/media/users/')
	password = models.CharField(max_length=300)

	# shows users active or not
	active = models.BooleanField(default=0)

	# important 100% interests
	interests =  models.TextField()
	subscribed = models.TextField()
	subscribers = models.TextField()
	playlists =  models.TextField()

	# another playlist style liked posts and watched mosts
	liked_posts = models.TextField(default='[]')

	# time stuff
	registered_time = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	last_login = models.DateTimeField(null=True, blank=True)
	last_logout = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.username

	def return_how_much_time_passive(self):
		return last_login - registered_time

	@property
	def get_liked_posts(self):
		return json.loads(self.liked_posts)

	@property
	def get_subscribed(self):
		if not self.subscribed:
			return []
		try:
			return json.loads(self.subscribed)
		except json.JSONDecodeError:
			return []

	def liked_posts_add(self, obj):
		posts = json.loads(self.liked_posts)
		posts = list(posts)
		posts.append(obj)
		posts = json.dumps(posts)
		self.liked_posts = posts

		return obj

	def liked_posts_remove(self, obj):
		posts = json.loads(self.liked_posts)
		print(posts)
		print(type(posts))
		posts = list(posts)
		posts.remove(obj)
		posts = json.dumps(posts)
		self.liked_posts = posts

		return obj

	def add_to_subscribed(self, ch_name):
		subscribed = None
		if self.subscribed:
			subscribed = json.loads(self.subscribed)
		else:
			subscribed = []
		subscribed = list(subscribed)
		subscribed.append(ch_name)
		subscribed = json.dumps(subscribed)
		self.subscribed = subscribed

		return ch_name


	def remove_from_subscribed(self, ch_name):
		subscribed = json.loads(self.subscribed)
		subscribed = list(subscribed)
		if ch_name not in subscribed:
			raise ObjectNotExistError(
				{
					'error': 'Object_NOT_EXISTS', 
					'field' : 'user.subscribed',
					'object' : 'channel name'
				}
			)
		subscribed.remove(ch_name)
		subscribed = json.dumps(subscribed)
		self.subscribed = subscribed

		return ch_name



# class Post(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	title = models.CharField(max_length=300)
# 	content = models.TextField(max_length=1000)
# 	image = models.ImageField(upload_to='static/media/posts/')
# 	created_time = models.DateTimeField(auto_now_add=True)
# 	updated_time = models.DateTimeField(auto_now=True) 

# 	public = models.BooleanField(default=1)

# 	# ulta important things
# 	likes = models.IntegerField()
# 	dislikes = models.IntegerField()
# 	views = models.IntegerField()

# 	def __str__(self):
# 		return self.title

# 	def get_statistic_data(self):
# 		return self.likes, self.dislikes, self.views

