from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.models import authentication
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password,check_password
from django.utils.html import strip_tags
import uuid
import random

# Create your views here.
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
        authentication.objects.create(
            v_id = unique_id,
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
    request.session['first_name'] = user_credentials.first().first_name
    request.session['last_name'] = user_credentials.first().last_name
    request.session['email'] = user_credentials.first().email
    
    return Response({'msg': 200})


@api_view(['POST'])
def logout(request):
    del request.session['v_id']
    del request.session['first_name']
    del request.session['last_name']
    del request.session['email']
    
    return Response({'msg' : 200})

#Modal controls
