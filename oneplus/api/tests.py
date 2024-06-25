import base64
import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Category, Tag


class TestUsers(TestCase):

	def setUp(self):
		self.client = Client()
		self.register = reverse('user-registeration')
		self.posts = reverse('post-operations')


	def test_register_user(self):
		response = self.client.post(
			self.register,
			json.dumps({
			    "username": "ola",
			    "password": "olapass",
			    "profile": {
			        "bio": "ola bio",
			        "picture_url": "http://picture.com/ola"
			    }
			}),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 201)


	def test_register_user_duplicate(self):
		first_response = self.client.post(
			self.register,
			json.dumps({
			    "username": "ola",
			    "password": "olapass",
			    "profile": {
			        "bio": "ola bio",
			        "picture_url": "http://picture.com/ola"
			    }
			}),
			content_type='application/json'
		)

		second_response = self.client.post(
			self.register,
			json.dumps({
			    "username": "ola",
			    "password": "olapass",
			    "profile": {
			        "bio": "ola bio",
			        "picture_url": "http://picture.com/ola"
			    }
			}),
			content_type='application/json'
		)

		self.assertEqual(first_response.status_code, 201)
		self.assertEqual(second_response.status_code, 400)



class TestPosts(TestCase):

	def setUp(self):
		self.client = Client()
		self.register = reverse('user-registeration')
		self.posts = reverse('post-operations')


	def test_list_posts_unauthenticated(self):
		response = self.client.get(
			self.posts,
		)
		self.assertEqual(response.status_code, 401)


	def test_list_posts_authenticated(self):
		register_user_response = self.client.post(
			self.register,
			json.dumps({
			    "username": "omar",
			    "password": "omarpass",
			    "profile": {
			        "bio": "omar bio",
			        "picture_url": "http://picture.com/omar"
			    }
			}),
			content_type='application/json'
		)

		list_posts_response = self.client.get(
			self.posts,
			headers={
				'Authorization': f'Basic {base64.b64encode(b"omar:omarpass").decode("utf-8")}'
			}
		)

		print(f'Basic {base64.b64encode(b"omar:omarpass").decode("utf-8")}')
		
		self.assertEqual(register_user_response.status_code, 201)
		self.assertEqual(list_posts_response.status_code, 200)
		self.assertEqual(list_posts_response.content.decode(), json.dumps([]))


	def test_add_posts(self):
		category = Category.objects.create(name='comedy')
		tag = Tag.objects.create(name='mytag')

		register_user_response = self.client.post(
			self.register,
			json.dumps({
			    "username": "omar",
			    "password": "omarpass",
			    "profile": {
			        "bio": "omar bio",
			        "picture_url": "http://picture.com/omar"
			    }
			}),
			content_type='application/json'
		)

		add_posts_response = self.client.post(
			self.posts,
			json.dumps({
			    "title": "my first post",
			    "content": "my first post content",
			    "author": 1,
			    "tags": [tag.id],
			    "categories": [category.id]
			}),
			content_type='application/json',
			headers={
				'Authorization': f'Basic {base64.b64encode(b"omar:omarpass").decode("utf-8")}'
			}
		)

		list_posts_response = self.client.get(
			self.posts,
			headers={
				'Authorization': f'Basic {base64.b64encode(b"omar:omarpass").decode("utf-8")}'
			}
		)

		print(f'Basic {base64.b64encode(b"omar:omarpass").decode("utf-8")}')
		
		self.assertEqual(register_user_response.status_code, 201)
		self.assertEqual(add_posts_response.status_code, 201)
		self.assertEqual(list_posts_response.status_code, 200)
		self.assertEqual(list_posts_response.content.decode(), json.dumps([{
			"title": "my first post",
			"content": "my first post content",
			"author": 1,
			"tags": [],
			"categories": []
		}]))