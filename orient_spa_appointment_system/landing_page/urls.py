from django.urls import path
from landing_page import views

urlpatterns = [
    path('', views.index, name='landing_page'),
    path('auth', views.auth, name='auth'),
    path('verification/', views.veification, name='verification'),
    path('validate_priv/', views.validate_priv, name='validate_priv'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('change_password_template/', views.change_password_template, name='change_password_template')
]
