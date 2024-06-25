from django.contrib import admin
from .models import Tag, Category

# registering default model admin interfaces for Tag and Category

admin.site.register(Tag)
admin.site.register(Category)