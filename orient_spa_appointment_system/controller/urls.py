from django.urls import path
from controller import views

urlpatterns = [
   path('signup/', views.signup, name='signup'),
   path('verify_account/', views.verify_account, name='verify_account'),
   path('signin/', views.signin, name='signin'),
   path('logout/', views.logout, name='logout')
]
