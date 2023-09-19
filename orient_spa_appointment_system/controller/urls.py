from django.urls import path
from controller import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('signup/', views.signup, name='signup'),
   path('verify_account/', views.verify_account, name='verify_account'),
   path('signin/', views.signin, name='signin'),
   path('logout/', views.logout, name='logout'),
   path('modal_content/', views.modal_content, name='modal_content'),
   path('modal_service/', views.modal_service, name="modal_service"),
   path('service_content/', views.service_content, name="service_content"),
   path('save_appointment/', views.save_appointment, name='save_appointment'),
   path('pending_appointments/', views.display_pending_appointment, name='pending_appointments'),
   path('canceled_appointments/', views.display_canceled_appointment, name='canceled_appointments'),
   path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
   path('save_service/', views.save_service, name='save_service'),
   path('employee_details/', views.employee_details, name='employee_details'),
   path('insert_dtr/', views.insert_dtr, name='insert_dtr'),
   path('delete_employee/', views.delete_employee, name='delete_employee'),
   path('employee_dtr/', views.employee_dtr, name='employee_dtr'),
   path('display_admin_pending/', views.display_admin_pending, name='display_admin_pending'),
   path('display_available_employee/', views.display_available_employee, name='display_available_employee'),
   path('confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
   path('display_admin_scheduled/', views.display_admin_scheduled, name='display_admin_scheduled'),
   path('notif/', views.sendEmail_txtNotif, name='notif'),
   path('payment_modal/', views.show_payment_modal, name='payment_modal'),
   path('confirm_payment/', views.confirm_payment, name='confirm_payment')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)