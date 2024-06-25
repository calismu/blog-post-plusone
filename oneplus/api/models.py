from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField()
	picture_url = models.URLField()

	def __str__(self):
		return self.user.username


class Category(models.Model):
	name = models.CharField(max_length = 50)
	slug = models.SlugField(max_length = 50, unique = True, null=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
			super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length = 50)
	slug = models.SlugField(max_length = 50, unique = True, null=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
			super(Tag, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Post(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField()
	author = models.OneToOneField(Profile, on_delete=models.SET_NULL, blank=True, null=True)
	categories = models.ManyToManyField(Category, related_name='posts', blank=True)
	tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	content = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.user.username