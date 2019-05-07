"""eattendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authenticate.views import password_reset_confirm, password_reset_complete, password_reset_done

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('authenticate/', include('authenticate.urls')),
    path('database/', include('database.urls')),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password/reset/complete', password_reset_complete, name='password_reset_complete'),
    path('password/reset/done', password_reset_done, name='password_reset_done'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
