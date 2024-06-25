from django.contrib import admin
from django.urls import path, include

# root url pattern '/api' preceeding all paths

urlpatterns = [
    path('api/', include('api.urls'), name='application'),
    path('admin/', admin.site.urls),
]
