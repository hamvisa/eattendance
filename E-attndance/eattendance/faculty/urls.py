from django.urls import path, include
from . import views

app_name = 'faculty'
urlpatterns = [
    path('home/', views.home, name='home'),

]
