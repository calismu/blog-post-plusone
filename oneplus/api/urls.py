from django.urls import path, include

from api.views import (
	PostView,
	CommentView,
	CategoryView,
	TagView,
	UserView
)


urlpatterns = [
	# POSTS
	path('posts', PostView.as_view(), name='post-operations'),
	path('posts/<int:post_id>', PostView.as_view(), name='post-details'),

	# COMMENTS
	path('comments', CommentView.as_view(), name='comment-operations'),
	path('comments/<int:comment_id>', CommentView.as_view(), name='comment-details'),

	# CATEGORIES
	path('categories', CategoryView.as_view(), name='category-operations'),

	# TAGS
	path('tags', TagView.as_view(), name='tag-operations'),

	# USER
	path('user/register', UserView.as_view(), name='user-registeration'),
]