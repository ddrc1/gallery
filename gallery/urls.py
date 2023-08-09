"""
URL configuration for gallery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as user
from photo import views as photo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', user.user_import),
    path('user/list_all/', user.user_list),

    path('photo/', photo.upload),
    path('photo/list/', photo.list_photos),
    path('photo/send/<int:photo_id>', photo.send_photo),
    path('photo/list_all/', photo.list_all_photos),
    path('photo/authorize/', photo.photo_authorize),
    path('photo/like/', photo.like),
    path('photo/comment/', photo.comment),
    path('photo/comment/list_all/', photo.list_all_comments),
    path('photo/comment/<int:photo_id>', photo.list_comments_by_photo),
]
