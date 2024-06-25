from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
	Profile,
	Category,
	Tag,
	Post,
	Comment
)


class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):

	# author and post keys to be used with commends, don't include actual model instances
	author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
	post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

	class Meta:
		model = Comment
		fields = ['id', 'content', 'author', 'post']

	def create(self, validated_data):
		'''Enable comment creation out of validated data from serializer'''
		comment = Comment.objects.create(**validated_data)
		return comment


class PostSerializer(serializers.ModelSerializer):

	# author, post, and tags keys to be used with commends, don't include actual model instances
	author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
	categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
	tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

	class Meta:
		model = Post
		fields = ['id', 'title', 'content', 'author', 'categories', 'tags']

	def create(self, validated_data):
		'''Enable creation of Posts through serializer'''
		tag_data = validated_data.pop('tags')
		category_data = validated_data.pop('categories')
		post = Post.objects.create(**validated_data)
		post.tags.set(tag_data)
		post.categories.set(category_data)
		return post


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['bio', 'picture_url']


class UserSerializer(serializers.ModelSerializer):
	# profile key to be used with commends, don't include actual model instances
	profile = ProfileSerializer(required=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'profile']

	def create(self, validated_data):
		'''Enable creation of Users through serializer'''
		profile_data = validated_data.pop('profile')
		user = User.objects.create_user(**validated_data)
		Profile.objects.create(user=user, **profile_data)
		return user