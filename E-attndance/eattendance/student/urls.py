from django.urls import path, include
from . import views

app_name = 'student'
urlpatterns = [
    path('home/', views.home, name='home'),

]
