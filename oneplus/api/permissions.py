from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
	'''Permission to allow unsafe methods only to Comment and Post owners'''

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.author.user == request.user