from django.urls import path
from controller import views

urlpatterns = [
   path('signup/', views.signup, name='signup'),
   path('verify_account/', views.verify_account, name='verify_account'),
   path('signin/', views.signin, name='signin'),
   path('logout/', views.logout, name='logout'),
   path('modal_content/', views.modal_content, name='modal_content'),
   path('save_appointment/', views.save_appointment, name='save_appointment'),
   path('pending_appointments/', views.display_pending_appointment, name='pending_appointments'),
   path('canceled_appointments/', views.display_canceled_appointment, name='canceled_appointments'),
   path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
   path('save_service/', views.save_service, name='save_service')
]
