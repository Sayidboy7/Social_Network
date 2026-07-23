from auth_network.models import User
from django.db import models
from taggit.managers import TaggableManager
import json

from django.urls import reverse


class LastestManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().order_by('-updated_time')


class PublicManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(public=True)


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	title = models.CharField(max_length=300)
	slug = models.SlugField(max_length=400)
	content = models.TextField(max_length=1000)
	image = models.ImageField(upload_to='static/media/posts/')
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True) 

	public = models.BooleanField(default=1)

	# ulta important things
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	views = models.IntegerField(default=0)

	tags = TaggableManager()
	objects = models.Manager()
	lastest = LastestManager()

	publics = PublicManager()

	def __str__(self):
		return self.title

	def get_statistic_data(self):
		return self.likes, self.dislikes, self.views


class History(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now=True)
	post_tags = models.TextField(blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		if self.post_id:
			self.post_tags = json.dumps(list(self.post.tags.names()))

			super().save(update_fields=['post_tags'])	


	def __str__(self):
		return f'{self.user} - {self.post} {self.time}'