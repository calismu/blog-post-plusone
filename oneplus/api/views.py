from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import (
	Profile,
	Category,
	Tag,
	Post,
	Comment
)
from .serializers import (
	TagSerializer,
	CategorySerializer,
	CommentSerializer,
	PostSerializer,
	UserSerializer,
)
from .permissions import (
	IsAuthorOrReadOnly,
)


class UserView(APIView):
	'''serializer operations on django default user instance'''

	permission_classes = [] #anon users can register

	def post(serlf, request):

		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
	'''Serializer operations on Category model'''

	def get(self, request):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)


class TagView(APIView):
	'''Serializer operations on Tag model'''
	
	def get(self, request):
		tags = Tag.objects.all()
		serializer = TagSerializer(tags, many=True)
		return Response(serializer.data)


class CommentView(APIView):
	'''Serializer operations on Commend model'''

	#user must have permission (owner of the comment) to edit it
	permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

	def get(self, request):
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, comment_id):
		try:
			comment = Comment.objects.get(id=comment_id)
		except Comment.DoesNotExist:
			return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

		self.check_object_permissions(request, comment)
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class PostView(APIView):
	'''Serializer operations on Post model'''

	#user must have permission (owner of the comment) to edit it
	permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

	def get(self, request, post_id=None):
		if post_id:
			try:
				post = Post.objects.get(id=post_id)
				serializer = PostSerializer(post)
			except Post.DoesNotExist:
				return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
		else:
			# Search and filter query params
			tag_name = request.query_params.get('tag')
			category_name = request.query_params.get('category')
			post_title = request.query_params.get('title')
			content_chunk = request.query_params.get('content')

			# filter 'posts' based on query params existance and values
			posts = Post.objects.all().order_by('id')
			if tag_name:
				posts = posts.filter(tags__slug=tag_name)
			if category_name:
				posts = posts.filter(categories__slug=category_name)
			if post_title:
				posts = posts.filter(title=post_title)
			if content_chunk:
				posts = posts.filter(content__contains=content_chunk)

			# instantiate, setup, and run paginator on posts list from model
			paginator = PageNumberPagination()
			paginator.page_size = 10			
			serializer = PostSerializer(paginator.paginate_queryset(posts, request), many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request):
		post_id = request.data.get('id')
		try:
			post = Post.objects.get(id=post_id)
		except Post.DoesNotExist:
			return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

		self.check_object_permissions(request, post)
		serializer = PostSerializer(post, data=request.data, partial=False)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, post_id):
		try:
			post = Post.objects.get(id=post_id)
		except Post.DoesNotExist:
			return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

		self.check_object_permissions(request, post)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)