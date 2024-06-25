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
	permission_classes = []

	def post(serlf, request):

		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):

	def get(self, request):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)


class TagView(APIView):
	
	def get(self, request):
		tags = Tag.objects.all()
		serializer = TagSerializer(tags, many=True)
		return Response(serializer.data)


class CommentView(APIView):

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

	permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

	def get(self, request, post_id=None):
		if post_id:
			try:
				post = Post.objects.get(id=post_id)
				serializer = PostSerializer(post)
			except Post.DoesNotExist:
				return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
		else:
			tag_name = request.query_params.get('tag')
			category_name = request.query_params.get('category')
			post_title = request.query_params.get('title')
			content_chunk = request.query_params.get('content')

			posts = Post.objects.all().order_by('id')
			if tag_name:
				posts = posts.filter(tags__slug=tag_name)
			if category_name:
				posts = posts.filter(categories__slug=category_name)
			if post_title:
				posts = posts.filter(title=post_title)
			if content_chunk:
				posts = posts.filter(content__contains=content_chunk)

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