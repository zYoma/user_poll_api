from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework import permissions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('user_poll.urls')),
]


schema_view = get_schema_view(
   openapi.Info(
      title="API для системы опросов пользователей",
      default_version='v1',
      description="Документация для приложения user_poll",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^api(?P<format>\.json|\.yaml)$',
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^api/$', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'),
]
