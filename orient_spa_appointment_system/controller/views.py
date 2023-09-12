from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.models import authentication,services, appointments
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password,check_password
from django.utils.html import strip_tags
from datetime import datetime
import uuid
import random

# Authentication backend
@api_view(['POST'])
def signup(request):
    data = request.data
    unique_id = uuid.uuid4()
    random_code = ''.join(random.choices('0123456789', k=4))
    
    email =  authentication.objects.filter(email = data['email'])
    
    if email.exists():
        return Response({'msg' : 'Email already in used'})
    
    if data['password'] != data['c_password']:
        return Response({'msg' : 'Passwords dont match'})
    elif len(data['password']) < 8:
        return Response({'msg' : 'Password requires 8 characters'})
    
    
    if data['priv'] == '2':
        html_message = render_to_string('email.html', 
                                        {'header': 'Verification code', 
                                         'title': 'Do not share This code to anyone.',
                                         'text': 'Thank you for supporting Orient SPA! This is your account verification code.',
                                         'code': random_code}
                                        )
    else:
        html_message = render_to_string('email.html', 
                                        {'header': 'Orient SPA Employment',
                                         'title': 'Orient SPA Account for Employee',
                                         'text': 'You are added as employee at Orient SPA! Use this email to login.',
                                         'code': ''
                                         }
                                        )
    plain_message = strip_tags(html_message)
        
    sent_count =send_mail(
        "Orient SPA account verification Code",
        plain_message,
        settings.EMAIL_HOST_USER,
        [data['email']],
        fail_silently=False,
        html_message=html_message
        )
    if sent_count == 1:    
        authentication.objects.create(
            v_id = unique_id,
            priv = int(data['priv']),
            first_name =  data['f_name'],
            last_name = data['l_name'],
            email = data['email'],
            password = make_password(data['password']),
            random_code = random_code
        )
        return Response({'msg' : 200, 'email' : data['email']})

@api_view(['POST'])
def verify_account(request):
    data = request.data
    
    check_code = authentication.objects.filter(email = data['email'], random_code = data['v_code'])
    
    if check_code:
        verify = authentication.objects.get(email = data['email'])
        verify.v_status = 'verified'
        verify.random_code = 0
        verify.save()
        
        return Response({'msg': 200})
    else:
        return Response({'msg' : 'Incorrect Verification Code'})
    
@api_view(['POST'])
def signin(request):
    data = request.data
    random_code = ''.join(random.choices('0123456789', k=4))
    
    user_credentials = authentication.objects.filter(email = data['email'])
    
    if not user_credentials.exists() or not check_password(data['password'], user_credentials.first().password):
        return Response({'msg': 'Incorrect email or password'})
    elif user_credentials.first().v_status == 'unverified':
        html_message = render_to_string('email.html', {'code': random_code})
        plain_message = strip_tags(html_message)
            
        sent_count =send_mail(
        "Orient SPA account verification Code",
        plain_message,
        settings.EMAIL_HOST_USER,
        [data['email']],
        fail_silently=False,
        html_message=html_message
        )      
        if sent_count == 1:
            new_code = authentication.objects.get(email = data['email'])
            new_code.random_code = random_code
            new_code.save()
            
            return Response({'msg': 400, 'email' : user_credentials.first().email})
    
    request.session['v_id'] = user_credentials.first().v_id
    request.session['priv'] = user_credentials.first().priv
    request.session['first_name'] = user_credentials.first().first_name
    request.session['last_name'] = user_credentials.first().last_name
    request.session['email'] = user_credentials.first().email
    
    return Response({'msg': 200})


@api_view(['POST'])
def logout(request):
    del request.session['v_id']
    del request.session['priv']
    del request.session['first_name']
    del request.session['last_name']
    del request.session['email']
    
    return Response({'msg' : 200})

#Appointment backend
@api_view(['POST'])
def save_appointment(request):
    data = request.data
    time = data['time']
    time_obj = datetime.strptime(time, '%H:%M')
    new_time = time_obj.strftime('%I:%M %p')
    
    validate_time = appointments.objects.filter(appointment_date = data['date'], appointment_time = new_time)
    service = services.objects.filter(id = data['service'])
    
    if not validate_time:
        appointments.objects.create(
            client_name = request.session['first_name']+' '+request.session['last_name'],
            client_email = request.session['email'],
            client_number = data['phone_num'],
            appointment_date = data['date'],
            appointment_time = new_time,
            service_id = data['service'],
            service_name = service.first().service_name,
            service_price = service.first().service_price
        )
        return Response({'msg' : 200})
    
    else:
        return Response({'msg' : 'Date and time not available'})

@api_view(['POST'])
def cancel_appointment(request):
    data = request.data
    html_message = render_to_string('email_template/cancelation.html', {'msg': data['reason']})
    plain_message = strip_tags(html_message)
            
    sent_count =send_mail(
    "Orient SPA Calapan",
    plain_message,
    settings.EMAIL_HOST_USER,
    [request.session['email']],
    fail_silently=False,
    html_message=html_message
    )      
    if sent_count == 1:
        appointment = appointments.objects.get(id = data['id'])
        appointment.appointment_status = 'Canceled'
        appointment.save()
        return Response({'msg': 200})

def display_pending_appointment(request):
    email = request.session['email']
    pending = appointments.objects.filter(client_email = email, appointment_status = 'Pending')
    return render(request, 'appointment/pending_appointments.html', {'response' : pending})

def display_canceled_appointment(request):
    email = request.session['email']
    canceled = appointments.objects.filter(client_email = email, appointment_status = 'Canceled')
    return render(request, 'appointment/canceled_appointment.html', {'response' : canceled})


#Modal controls
def modal_content(request):
    service = services.objects.all()
    return render(request, 'modal_content.html', {'services' : service})

def modal_service(request):
    return render(request, 'modal_service.html')


def service_content(request):
    service = services.objects.all()
    return render(request, 'services_templates/service_content.html', {'services' : service})

def save_service(request):
    services.objects.create(
        service_name = request.POST['service_name'],
        service_price = request.POST['price'],
        service_img = request.FILES['img'],
        service_description = request.POST['description']
    )
    
    return render(request, 'services.html', {'msg' : 'Service saved!'})