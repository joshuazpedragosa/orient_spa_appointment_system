from django.urls import path
from admin_side import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_employee/', views.admin_employee, name='add_employee')
]
