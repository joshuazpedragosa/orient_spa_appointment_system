from django.urls import path
from client_side import views

urlpatterns = [
    path('', views.home, name='home'),
    path('appointment/', views.appointment, name='appointment'),
    path('services/', views.services, name='services'),
    path('chat/', views.chat, name='chat'),
    path('settings/', views.settings, name='settings'),
]
