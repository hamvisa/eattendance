from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'authenticate'
urlpatterns = [
    path('logout/', views.my_logout, name='logout'),
    path('login/', views.my_login, name='login'),
    path('password/change/', views.my_change_password, name='change_password'),
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='reg/password_reset_form.html'),
         name='password_reset'),
    path('password/reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='reg/password_reset_done.html'),
         name='password_reset_done'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reg/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password/reset/complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='reg/password_reset_complete.html'),
         name='password_reset_complete'),

]
