from django.urls import path
from landing_page import views

urlpatterns = [
    path('', views.index, name='landing_page'),
    path('auth', views.auth, name='auth'),
    path('verification/', views.veification, name='verification'),
    path('validate_priv/', views.validate_priv, name='validate_priv')
]
