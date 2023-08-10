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
from account import views as account
from photo import views as photo
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for your Argo Tech test",
    ),
    public=True,
    #permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),

    path('user/', account.user_import),
    path('user/list_all/', account.user_list),

    path('photo/', photo.upload),
    path('photo/list/', photo.list_photos),
    path('photo/send/<int:photo_id>', photo.send_photo),
    path('photo/list_all/', photo.list_all_photos),
    path('photo/authorize/', photo.photo_authorize),
    path('photo/like/', photo.like),
    path('photo/comment/', photo.comment),
    path('photo/comment/list_all/', photo.list_all_comments),
    path('photo/comment/<int:photo_id>', photo.list_comments_by_photo),

    path('swagger/schema', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]
