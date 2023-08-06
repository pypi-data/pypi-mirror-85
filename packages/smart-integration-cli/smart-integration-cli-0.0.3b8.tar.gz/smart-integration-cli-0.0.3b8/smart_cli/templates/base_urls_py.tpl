from django.contrib import admin
from django.urls import path, include
from {{ params['app_name'] }} import urls as api_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]