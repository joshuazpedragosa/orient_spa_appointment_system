from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password,check_password
from django.utils.html import strip_tags
from django.db.models import Sum
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
                                         'text': 'You are added as employee at Orient SPA! Use this email to login. Password : '+data['password'],
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
    
    if not user_credentials.exists() or not check_password(data['password'], user_credentials.first().password) or user_credentials.first().priv == 3:
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
    
    appointment = appointments.objects.get(id = data['id'])
    
    if 'canceled_by' in data:
        sent_count =send_mail(
        "Orient SPA Calapan",
        plain_message,
        settings.EMAIL_HOST_USER,
        [appointment.client_email],
        fail_silently=False,
        html_message=html_message
        )    
    else:
        sent_count =send_mail(
        "Orient SPA Calapan",
        plain_message,
        settings.EMAIL_HOST_USER,
        [request.session['email']],
        fail_silently=False,
        html_message=html_message
        )      
        
    if sent_count == 1:
        appointment.appointment_status = 'Canceled'
        appointment.save()
        return Response({'msg': 200})
    else:
        return Response({'msg': 'Network error. Please try again'})

def display_pending_appointment(request):
    email = request.session['email']
    pending = appointments.objects.filter(client_email = email, appointment_status = 'Pending')
    service = services.objects.all()
    return render(request, 'appointment/pending_appointments.html', {'response' : pending, 'services' : service})

def display_canceled_appointment(request):
    month = request.GET['a']
    year = request.GET['b']
    email = request.session['email']
    canceled = appointments.objects.filter(client_email = email, appointment_status = 'Canceled')
    service = services.objects.all()
    return render(request, 'appointment/canceled_appointment.html', {'response' : canceled, 'services' : service, 'month' : month, 'year' : year})

def display_done_appointment(request):
    month = request.GET['a']
    year = request.GET['b']
    email = request.session['email']
    done = appointments.objects.filter(client_email = email, appointment_status = 'Done').values()
    
    for y in done:
        app_id = y['id']
        
    emp_sched = employee_schedule.objects.filter(appointment_id = app_id).values()
    service = services.objects.all()
    return render(request, 'appointment/done_appointment.html', {'response' : done, 'services' : service, 'emp' : emp_sched, 'month' : month, 'year' : year})

def display_confirmed_appointment(request):
    email = request.session['email']
    app = appointments.objects.filter(client_email = email, appointment_status = 'Confirmed')
    service = services.objects.all()
    sched = employee_schedule.objects.all()
    emp = authentication.objects.filter(priv = 3).values()
    return render(request, 'appointment/confirmed_appointment.html', {'appointment' : app, 'services' : service, 'sched' :sched, 'emp' : emp})

@api_view(['POST'])
def save_rating(request):
    data = request.data
    
    app = appointments.objects.filter(id = data['app_id']).values()
    
    for x in app:
        service_id = x['service_id']

    ratings_comments.objects.create(
        user_id = request.session['v_id'],
        service_id = service_id,
        comments = data['comment'],
        ratings = data['rate']
    )
    
    sched = employee_schedule.objects.get(appointment_id = data['app_id'])
    sched.status = 'Rated'
    sched.save()
    
    return Response({'msg' : 200})
    

#Admin appointment functions
def display_admin_pending(request):
    app = appointments.objects.filter(appointment_status = 'Pending')
    service = services.objects.all()
    return render(request, 'admin_appointments/admin_pending.html', {'appointment' : app, 'services' : service})

def display_admin_scheduled(request):
    app = appointments.objects.filter(appointment_status = 'Confirmed')
    service = services.objects.all()
    sched = employee_schedule.objects.all()
    emp = authentication.objects.filter(priv = 3).values()
    return render(request, 'admin_appointments/admin_scheduled.html', {'appointment' : app, 'services' : service, 'sched' : sched, 'emp' : emp})

def display_admin_done(request):
    month = request.GET['a']
    year = request.GET['b']
    
    app = appointments.objects.filter(appointment_status = 'Done')
    service = services.objects.all()
    sched = employee_schedule.objects.all()
    emp = authentication.objects.filter(priv = 3).values()
    return render(request, 'admin_appointments/admin_done.html', {'appointment' : app, 'services' : service, 'sched' : sched, 'emp' : emp, 'month' : month, 'year' : year})

def display_available_employee(request):
    appointment_id = request.GET['id']
    
    employee = authentication.objects.filter(priv = 3).values()
    appointment = appointments.objects.filter(id = appointment_id).values()
    
    for a in appointment:
        target_date = a['appointment_date']
        target_time = a['appointment_time']
        
        from_sched = employee_schedule.objects.filter(time=target_time , date=target_date).values()
        
    return render(request, 'modal_available_employee.html', {'emp' : employee, 'sched' : from_sched, 'id' : appointment_id})
        

@api_view(['POST'])
def confirm_appointment(request):
    data = request.data
    
    get_appointment = appointments.objects.get(id = data['app_id'])
    try:
        check_confirmed_appointment = employee_schedule.objects.get(appointment_id = data['app_id'])
    
        if get_appointment.appointment_status == 'Confirmed' and check_confirmed_appointment.employee_vid != data['employee']:
            check_confirmed_appointment.employee_vid = data['employee']
            check_confirmed_appointment.save()
            
            return Response({'msg' : 200})
        else:
            return Response({'msg' : 'Appointment was canceled or already confirmed.'})
    except employee_schedule.DoesNotExist:
        if get_appointment.appointment_status == 'Pending':
            get_appointment.appointment_status = 'Confirmed'
            get_appointment.save()
            
            employee_schedule.objects.create(
                employee_vid = data['employee'],
                appointment_id = data['app_id'],
                time = get_appointment.appointment_time,
                date = get_appointment.appointment_date
            )
            
            return Response({'msg' : 200})
    
def show_payment_modal(request):
    appointment_id = request.GET['id']
    
    appointment = appointments.objects.filter(id = appointment_id).values()
    sched = employee_schedule.objects.filter(appointment_id = appointment_id).values()
    for x in sched:
        stat = x['status']
    return render(request, 'admin_appointments/paymentModal.html', {'details' : appointment, 'id' : appointment_id, 'stat' : stat})

@api_view(['POST'])
def confirm_payment(request):
    data = request.data
    sched = employee_schedule.objects.get(appointment_id = data['id'])
    sched.status = 'Paid'
    sched.save()
    
    return Response({'msg' : 200})


@api_view(['POST'])
def mark_as_done(request):
    data = request.data
    
    app = appointments.objects.get(id = data['id'])
    app.appointment_status = 'Done'
    app.save()
    
    return Response({'msg' : 200})

@api_view(['POST'])
def sendEmail_txtNotif(request):
    data = request.data
    email = authentication.objects.filter(v_id = data['employee']).values()
    appointment = appointments.objects.filter(id = data['app_id']).values()
        
    html_message = render_to_string('email.html', 
                                    {'header': 'Orient SPA Schedule',
                                    'title': 'New Schedule',
                                    'header': 'Details',
                                    'details' : appointment,
                                    }
                                    )
    plain_message = strip_tags(html_message)
    
    for e in email:
        employee_email = e['email']
            
    sent_count =send_mail(
        "Orient SPA Schedule",
        plain_message,
        settings.EMAIL_HOST_USER,
        [employee_email],
        fail_silently=False,
        html_message=html_message
        )
        
    if sent_count == 1:
        message = render_to_string('email.html', 
                                    {'header': 'Orient SPA Schedule',
                                    'title': 'Appointment Confirmed',
                                    'details' : appointment,
                                    'employee' : email
                                    }
                                    )
        plain_message_1 = strip_tags(message)
        for x in appointment:
            client_email = x['client_email']
            
        sent_count = send_mail(
        "Orient SPA Appointment",
        plain_message_1,
        settings.EMAIL_HOST_USER,
        [client_email],
        fail_silently=False,
        html_message=message
        )
        return Response({'msg': 'Email Sent'})

#Modal controls
def modal_content(request):
    service = services.objects.filter(service_status = 'active').values()
    return render(request, 'modal_content.html', {'services' : service})

def modal_service(request):
    return render(request, 'modal_service.html')


def service_content(request):
    service = services.objects.all()
    return render(request, 'services_templates/service_content.html', {'services' : service})

def ratings(request):
    service_id = request.GET['a']
    service = services.objects.filter(id = service_id).values()
    rate = ratings_comments.objects.filter(service_id = service_id).values()
    total_sum = rate.aggregate(total = Sum('ratings'))['total']
    avg_ratings = 0
    
    if total_sum is None:
        total_sum = 0
        
    if total_sum > 0:
        avg_ratings = total_sum / len(rate)
    
    return render(request, 'services_templates/comment_rating.html', {'service' : service, 'rate' : rate, 'avg' : avg_ratings})

def comments(request):
    rate = request.GET['a']
    s_id = request.GET['b']
    
    comment = ratings_comments.objects.filter(ratings = rate, service_id = s_id).values()
    client = authentication.objects.all()
    reply = replies_comment.objects.all()
    return render(request, 'services_templates/comments.html', {'comment' : comment, 'client' : client, 'reply' : reply})

def save_service(request):
    services.objects.create(
        service_name = request.POST['service_name'],
        service_price = request.POST['price'],
        service_img = request.FILES['img'],
        service_description = request.POST['description']
    )
    
    return render(request, 'services.html', {'msg' : 'Service saved!'})

@api_view(['POST'])
def update_availability(request):
    data = request.data

    service = services.objects.filter(id = data['s_id']).values()
    for x in service:
        status = x['service_status']
        
    if status == 'active':
        stat = services.objects.get(id = data['s_id'])
        stat.service_status = 'inactive'
        stat.save()
        return Response({'msg' : 200})
        
    else:
        stat = services.objects.get(id = data['s_id'])
        stat.service_status = 'active'
        stat.save()
        return Response({'msg' : 200})

def modal_service_details(request):
    service_id = request.GET['id']
    
    service_details = services.objects.filter(id = service_id).values()
    
    return render(request, 'services_templates/modal_details.html', {'service_details' : service_details})

@api_view(['POST'])
def udpate_service_details(request):
    data = request.data
    
    check_service = services.objects.filter(id = data['service_id'], 
                                            service_name = data['name_update'],
                                            service_price = data['price_update'],
                                            service_description = data['description_update'])
    
    if check_service:
        return Response({'msg' : 'No changes applied.'})
    else:
        service = services.objects.get(id = data['service_id'])
        service.service_name = data['name_update']
        service.service_price = data['price_update']
        service.service_description = data['description_update']
        service.save()
        
        return Response({'msg' : 200})

@api_view(['POST'])    
def deletService(request):
    data = request.data
    admin_email = request.session['email']
    
    admin_auth = authentication.objects.filter(email = admin_email).values()
    
    for auth in admin_auth:
        admin_password = auth['password']
        
        if check_password(data['admin_pass'], admin_password):
            service = services.objects.filter(id = data['service_id'])
            service.delete()
            return Response({'msg' : 200})
        else:
            return Response({'msg' : 'Invalid Password!'})
    
@api_view(['POST'])
def save_reply(request):
    data = request.data
    
    replies_comment.objects.create(
        u_id = request.session['v_id'],
        comment_id = data['id'],
        replies = data['reply']
    )
    
    comment = ratings_comments.objects.get(id = data['id'])
    comment.replied = 'true'
    comment.save()
    
    return Response({'msg' : 200})

#Employee details rendering

def employee_details(request):
    date = request.GET['a']
    employee = authentication.objects.filter(priv = 3)
    dtr = dtr_record.objects.filter(date = date).values()
    
    return render(request, 'employee/employee_details.html', {'emp' : employee, 'dtr' : dtr})


#Employee backend (DTR Control)

@api_view(['POST'])
def insert_dtr(request):
    data = request.data
    
    record = dtr_record.objects.filter(employee_vid = data['emp_vid'], date = data['date']).values()
    
    if not record and data['dtr_type'] == 'morning':
        dtr_record.objects.create(
            employee_vid = data['emp_vid'],
            am_in = data['time'],
            date = data['date'],
            month = data['month']
        )
        
        return Response({'msg' : 200})
    
    elif not record and data['dtr_type'] == 'afternoon':
        dtr_record.objects.create(
            employee_vid = data['emp_vid'],
            pm_in = data['time'],
            date = data['date'],
            month = data['month']
        )
        
        return Response({'msg' : 200})
    
    elif record and data['dtr_type'] == 'morning' or record and data['hour'] == 12 and data['minutes'] <= 30:
        for x in record:
            am_time_out = x['am_out']
            
            if am_time_out == '':
                update_dtr = dtr_record.objects.get(employee_vid = data['emp_vid'], date = data['date'])
                update_dtr.am_out = data['time']
                update_dtr.save()
                
                return Response({'msg' : 200})
            else:
                return Response({'msg' : 'You have already used DTR. Please wait for the afternoon time in record.'})
    
    elif record and data['dtr_type'] == 'afternoon':
        for y in record:
            pm_time_in = y['pm_in']
            pm_time_out = y['pm_out']
            
            if pm_time_in == '' and pm_time_out == '':
                update_dtrpm = dtr_record.objects.get(employee_vid = data['emp_vid'], date = data['date'])
                update_dtrpm.pm_in = data['time']
                update_dtrpm.save()
                
                return Response({'msg' : 200})
            
            elif pm_time_in != '' and pm_time_out == '':
                update_dtrpm = dtr_record.objects.get(employee_vid = data['emp_vid'], date = data['date'])
                update_dtrpm.pm_out = data['time']
                update_dtrpm.save()
                
                return Response({'msg' : 200})
            
            else:
                return Response({'msg' : 'You have already used DTR. Please wait for tomorrow time in record.'})
    
    else:
        return Response({'msg' : 'Cannot use DTR at the moment. Please try again later'})

#remove employee
@api_view(['POST'])
def delete_employee(request):
    data = request.data
    
    confirm_admin = authentication.objects.filter(v_id = request.session['v_id']).values()
    employee = authentication.objects.filter(v_id = data['u_id'])
    
    for admin in confirm_admin:
        password = admin['password']
        
        if check_password(data['adminpass'], password):
           if employee.exists():
                employee.delete()
                return Response({'msg' : 200})
           else:
                return Response({'msg' : 'Employee not found.'})
        else:
            return Response({'msg' : 'Incorrect Password'})
        
#display employee dtr card
def employee_dtr(request):
    v_id = request.GET['a']
    selected_month = request.GET['b']
    year = request.GET['c']
    employee = authentication.objects.filter(v_id = v_id).values()
    dtr_rec = dtr_record.objects.filter(employee_vid = v_id).values()
    
    return render(request, 
                  'employee/dtr_records.html', 
                  {'emp' : employee, 
                   'dtr' : dtr_rec, 
                   'month' : selected_month,
                   'year' : year})
    
def displayMonthlyRate(request):
    user_verification_id = request.GET['v_id']
    employee = authentication.objects.filter(v_id = user_verification_id).values()
    
    return render(request, 'employee/monthly_rate.html',{'employee' : employee})

def calculate_salary(request):
    v_id = request.GET['id']
    rate = request.GET['rate']
    month = request.GET['month']
    
    records = dtr_record.objects.filter(employee_vid = v_id, month = month).values()
    record_count = records.count()
    
    amount = int(rate) * record_count
    late_hours = 0
    
    for x in records:
        time_am = x['am_in'].split(":")
        out_am = x['am_out'].split(":")
        time_pm = x['pm_in'].split(":")
        out_pm = x['pm_out'].split(":")
        
        if len(out_am) == 2 and len(time_am) == 2 and len(time_pm) == 2 and len(out_pm) == 2:
           try:
               am_out = int(out_am[0])
               am_in = int(time_am[0])
               pm_in = int(time_pm[0])
               pm_out = int(out_pm[0])
               
               if am_in < 8:
                   am_in = am_in + 1
               elif not am_in:
                   am_in = 0
               elif not am_out:
                   am_out = 0
               elif am_in and not am_out:
                   am_in = 0
                   am_out = 0
                   
               if pm_in == 12:
                   pm_in = 1
               elif not pm_in:
                   pm_in = 0
               elif not pm_out:
                   pm_out = 0
               elif pm_in and not pm_out:
                   pm_in = 0
                   pm_out = 0
               
               am_hour = am_out - am_in
               pm_hour = pm_out - pm_in
               
               working_hour = am_hour + pm_hour
               
               if working_hour > 8:
                   working_hour = 8
                   
               late = 8 - working_hour
               
               
               
               late_hours += late
           except ValueError:
               pass
    
    late_amount = late_hours * 60
    total_salary = amount - late_amount
    
    context = {
        'rate' : rate,
        'record_count' : record_count,
        'amount' : amount,
        'late_hours' :late_hours,
        'late_amount' : late_amount,
        'total' : total_salary
    }
    
    return render(request, 'employee/salary_report.html', context)