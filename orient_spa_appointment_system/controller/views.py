from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from controller.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password,check_password
from django.utils.html import strip_tags
from django.db.models import Sum
from datetime import datetime
from .sms_utility import send_sms
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
            client_number = data['phone_number'],
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
    _done = appointments.objects.filter(client_email = email, appointment_status = 'Done').values()
    _sched = employee_schedule.objects.all().values()
    _service = services.objects.all().values()
    _done_appointment_data_set = []
    
    for done_appointment in _done:
       _appointment_id = 0 
       _service_image = ''
       _service_name = ''
       _service_price = 0
       _date_appointed = ''
       _time_appointed = ''
       _status = ''
       
       _appointment_date = done_appointment['appointment_date']
       splited_date = _appointment_date.split("-")
       
       _year = int(splited_date[0])
       _month = int(splited_date[1])
       
       if _month == int(month) and _year == int(year):
            for schedules in _sched:
                if done_appointment['id'] == schedules['appointment_id']:
                    _appointment_id += schedules['appointment_id']
                    _date_appointed += schedules['date']
                    _time_appointed += schedules['time']
                    _status += schedules['status']
                    for service in  _service:
                        if done_appointment['service_id'] == service['id']:
                            _service_image += service['service_img']
                            _service_name += service['service_name']
                            _service_price += service['service_price']
        
        
       if _appointment_id != 0:                    
            _done_appointment_data_set.append({
                'id' : _appointment_id,
                'service_image' : _service_image,
                'service_name' : _service_name,
                'service_price' : _service_price,
                'date' : _date_appointed,
                'time' : _time_appointed,
                'status' : _status
                })
       
    context = {
         'appointment_data_set' : _done_appointment_data_set
     }  
        
    return render(request, 'appointment/done_appointment.html', context)

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
            
            sms_header = 'Your appointment was confirmed!'
            sms_message = (
                f"Good Day! Your appointment to our service ({appointments.service_name}) "
                f"was confirmed. Schedule Details: {appointments.appointment_date} "
                f"({appointments.appointment_time})"
            )

            html_message = render_to_string('email_template/text_message.html', {'header': sms_header, 'msg': sms_message, 'name' : appointments.client_name})
            plain_message = strip_tags(html_message)
            
            recipient = get_appointment.client_number
            
            send_sms(plain_message, recipient)
            
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
        
    _get_employment_data = employment_data.objects.filter(employee_v_id = user_verification_id).values()
    
    
    salary = 0
    
    for data in _get_employment_data:
        salary += data['basic_monthly_pay']
        break
    
    return render(request, 'employee/monthly_rate.html',{'employee' : employee, 'salary' : salary})

def calculate_salary(request):
    v_id = request.GET['id']
    rate = request.GET['rate']
    month = request.GET['month']
    year = request.GET['year']
    
    records = dtr_record.objects.filter(employee_vid = v_id, month = month+''+year).values()
    _count = records.count()
    
    employee_name = ''
    record_count = _count
    late_hours = 0
    late_minutes = 0
    early_out_amount = 0
    
    employee = authentication.objects.filter(v_id = v_id).values()
    
    for name in employee:
        employee_name += name['first_name'] + ' ' + name['last_name']
    
    for x in records:
        record_am_in = x['am_in']
        record_am_out= x['am_out']
        record_pm_in = x['pm_in']
        record_pm_out = x['pm_out']
        
        if record_am_in != '' and record_am_out == '' or record_pm_in != '' and record_pm_out == '':
            record_count = record_count -1
        elif record_am_in == '' and record_am_out == '' and record_pm_in != '' and record_pm_out != '':
            record_am_in = "00:00 am"
            record_am_out = "00:00 pm"
        elif record_am_in != '' and record_am_out != '' and record_pm_in == '' and record_pm_out == '':
            record_pm_in = "00:00 pm"
            record_pm_out = "00:00 pm"
        elif record_am_in != '' and record_am_out == '' and record_pm_in != '' and record_pm_out != '':
            record_am_in = "00:00 am"
            record_am_out = "00:00 pm"
        elif record_am_in != '' and record_am_out != '' and record_pm_in != '' and record_pm_out == '':
            record_pm_in = "00:00 am"
            record_am_out = "00:00 pm"
            
        new_am_in = record_am_in.split(":")
        new_am_out = record_am_out.split(":")
        new_pm_in = record_pm_in.split(":")
        new_pm_out = record_pm_out.split(":")
        
        #make sure if all required data is !null        
        if len(new_am_in) == 2 and len(new_am_out) == 2 and len(new_pm_in) == 2 and len(new_pm_out) == 2:
           try:
               #hours converted to integer
               hour_am_out = int(new_am_out[0])
               _hour_am_in = int(new_am_in[0])
               _hour_pm_in = int(new_pm_in[0])
               hour_pm_out = int(new_pm_out[0])
               
               hour_am_in = _hour_am_in
               hour_pm_in = _hour_pm_in
               
               #minutes converted to integer
               mins_am_out = int(new_am_out[1][:-2])
               mins_am_in = int(new_am_in[1][:-2])
               mins_pm_in = int(new_pm_in[1][:-2])
               mins_pm_out = int(new_pm_out[1][:-2])
               
               #check if time calculation starts at 8am and 1pm
               if hour_am_in < 8 and hour_am_in != 0:
                   hour_am_in = hour_am_in + 1
                   
               if hour_pm_in == 12:
                   hour_pm_in = 1
               
               #calculate lates sa time in per hour (am and pm)
               am_hour = hour_am_out - hour_am_in
               pm_hour = hour_pm_out - hour_pm_in
               working_hour = am_hour + pm_hour
               
               #pagcheck if maximum of 8 hours a day ang calculation ng salary
               if working_hour > 8:
                   working_hour = 8
               
               #pag get ng late in hours        
               hr_late = 8 - working_hour
               
               #pag minus noong day if yung dtr ay walang time out o nag cut ng dtr
               if am_hour == 0 and pm_hour == 0:
                   record_count = record_count - 1
                   hr_late = hr_late - 8
               else:
                    #calculate lates sa time in per minutes (am and pm)
                    if _hour_am_in >= 8:
                        late_minutes +=  mins_am_in
                        if late_minutes > 59:
                            late_hours += 1
                            late_minutes -= 60
                            
                    if _hour_pm_in >= 1 and _hour_pm_in != 12:
                        late_minutes += mins_pm_in
                        if late_minutes > 59:
                            late_hours += 1
                            late_minutes -= 60
                            
                    #calculate excess minutes before early out (am and pm)
                    if hour_am_out < 12 and hour_am_out != 0:
                        am_early_out_deduction = 60 - mins_am_out
                        early_out_amount += am_early_out_deduction
                        
                    if hour_pm_out < 5 and hour_pm_out != 0:
                        pm_early_out_deduction = 60 - mins_pm_out
                        early_out_amount += pm_early_out_deduction
               
               #add ng late sa main variable kada loop    
               late_hours += hr_late
               
           except ValueError:
               pass
    
    amount = int(rate) * record_count
    late_amount = late_hours * 60
    total_late_amount = late_amount + late_minutes
    partial_total_salary = amount - total_late_amount 
    total_salary = partial_total_salary - early_out_amount
    
    context = {
        'rate' : rate,
        'record_count' : record_count,
        'amount' : amount,
        'late_hours' : late_hours,
        'late_minutes' : late_minutes,
        'late_amount' : total_late_amount,
        'early_out_amount' : early_out_amount,
        'total' : total_salary,
        'month' : month,
        'employee_name' : employee_name
    }
    
    return render(request, 'employee/salary_report.html', context)

#get data to load in dashboard main cards
def load_dashboard_main_cards(request):
    _appointments = appointments.objects.all()
    _pending_appointments = appointments.objects.filter(appointment_status = 'Pending')
    _canceled_appointments = appointments.objects.filter(appointment_status = 'Canceled')
    _employees = authentication.objects.filter(priv = 3)
    
    total_appointments = _appointments.count()
    total_pending_appointments = _pending_appointments.count()
    total_canceled_appointments = _canceled_appointments.count()
    total_employees = _employees.count()
    
    context = {
        'total_appointments': total_appointments,
        'total_pending_appointments' : total_pending_appointments,
        'total_canceled_appointments' : total_canceled_appointments,
        'total_employees' : total_employees
    }
    
    return render(request, 'admin_dashboard_templates/dashboard_cards.html', context)

#get sales and revenues data and load to dashboard
def load_sales_revenue(request):
    #get monthly income and increase percentage
    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_year = current_datetime.year
    current_day = current_datetime.day
    
    #weekly income
    total_weekly_income = 0
    
    #income this month
    total_monthly_income = 0
    
    #annual income
    total_annual_income = 0
    
    #income last week
    total_income_last_week = 0
    
    #income last month
    total_income_last_month = 0
    
    #income last year
    total_income_last_year = 0
    
    #weekly ratings
    weekly_rating = 0
    
    #income increase or decrease rating
    income_rating = 0
    
    #annual ratings
    annual_rating = 0
    
    #canceled appointment in current month
    canceled_current_month = 0
    
    #canceled appointment last month
    canceled_last_month = 0
    
    #appointment canceled rating
    canceled_rating = 0
    
    app_data = appointments.objects.all().values()
    
    for n in app_data:
        appointment_date = n['appointment_date']
        appointment_status = n['appointment_status']
        _price = n['service_price']
        
        splited_date = appointment_date.split("-")
        
        year = int(splited_date[0])
        month = int(splited_date[1])
        day = int(splited_date[2])
        
        if year == current_year:
            if appointment_status == 'Done':
                total_annual_income += _price
                
        if year == (current_year - 1):
            if appointment_status == 'Done':
                total_income_last_year += _price
        
        #weekly calculation        
        if current_day >= 7 and current_month == month:
            start_day = current_day - 7
            
            for x in range((start_day + 1), (current_day + 1)):
                 if x == day:
                     total_weekly_income += _price
                     break
        
        # weekly calculation for month between February and March
        if current_day < 7 and current_month == 3:
            month_excess_days = 7 - current_day
            start_day_last_month = 29 - month_excess_days
            
            for x in range((start_day_last_month + 1), 30):
                if x > day and x <= 29 and (month - 1) == 2:
                    total_weekly_income += _price
                    break
                    
            for x in range(1, (current_day + 1)):
                if x >= 1 and x <= day:
                    total_weekly_income += _price
                    break
                
        #calculate total income last week
        if current_day >= 14 and current_month == month:
            start_day_last = current_day - 14
            
            for x in range((start_day_last + 1), (current_day - 6)):
                if x == day:
                    total_income_last_week += _price
                    break
        
        if year == current_year and month == current_month:
            if appointment_status == 'Done':
                total_monthly_income += _price
                
            if appointment_status == 'Canceled':
                canceled_current_month += 1
        
        if current_month == 1:        
            if year == (current_year - 1) and month == 12:
                if appointment_status == 'Done':
                    total_income_last_month += _price
                    
                if appointment_status == 'Canceled':
                    canceled_last_month += 1
        else:
            if year == current_year and month == (current_month - 1):
                if appointment_status == 'Done':
                    total_income_last_month += _price
                    
                if appointment_status == 'Canceled':
                    canceled_last_month += 1
    
    #weekly ratings
    if total_weekly_income != 0:
        if total_weekly_income >= total_income_last_week:
            weekly_product = total_income_last_week * 100
            weekly_percent = weekly_product / total_weekly_income
            weekly_rating += 100 - weekly_percent
        else:
            _weekly_product = total_weekly_income * 100
            _weekly_percent = _weekly_product / total_income_last_week
            weekly_rating += 100 - _weekly_percent
    elif total_weekly_income == 0 and total_income_last_week != 0:
        weekly_rating += 100
       
    #monthly ratings             
    if total_monthly_income != 0:
        if total_monthly_income >= total_income_last_month:
            product = total_income_last_month * 100
            percent = product / total_monthly_income
            income_rating += 100 - percent
        else:
            _product = total_monthly_income * 100
            _percent = _product / total_income_last_month
            income_rating += 100 - _percent
    elif total_monthly_income == 0 and total_income_last_month != 0:
        income_rating += 100
        
    #annual ratings
    if total_annual_income != 0:
        if total_annual_income >= total_income_last_year:
            annual_product = total_income_last_year * 100
            annual_percent = annual_product / total_annual_income
            annual_rating = 100 - annual_percent
        else:
            _annual_product = total_annual_income * 100
            _annual_percent = _annual_product / total_income_last_year
            annual_rating = 100 - _annual_percent
    elif total_annual_income == 0 and total_income_last_year != 0:
        annual_rating = 100

    #Get overall services ratings
    _ratings = ratings_comments.objects.all().values()
    total_ratings_number = _ratings.count()
    ratings_sum = 0
    _total_rating = 0
    
    for x in _ratings:
        ratings_sum += x['ratings']
    
    if ratings_sum != 0 and total_ratings_number != 0:
        _total_rating = ratings_sum / total_ratings_number
    
    #get monthly canceled appointment ratings comparing last month and present
    if canceled_current_month != 0:
        if canceled_current_month > canceled_last_month:
            canceled_product = canceled_last_month * 100
            canceled_percent = canceled_product / canceled_current_month
            canceled_rating += 100 - canceled_percent
        else:
            _canceled_product = canceled_current_month * 100
            _canceled_percent = _canceled_product / canceled_last_month
            canceled_rating += 100 - _canceled_percent
    elif canceled_current_month == 0 and canceled_last_month != 0:
        canceled_rating += 100
    
    context = {
        'total_weekly_income' : total_weekly_income,
        'total_monthly_income' : total_monthly_income,
        'total_annual_income' : total_annual_income,
        'total_income_last_week' : total_income_last_week,
        'total_income_last_year' : total_income_last_year,
        'weekly_rating' : weekly_rating,
        'income_rating' : income_rating,
        'annual_rating' : annual_rating,
        'total_monthly_income' : total_monthly_income,
        'total_income_last_month' : total_income_last_month,
        'rating' : _total_rating,
        'canceled_rating' : canceled_rating,
        'canceled_current_month' : canceled_current_month,
        'canceled_last_month' : canceled_last_month
    }
    
    return render(request, 'admin_dashboard_templates/sales_revenue.html', context)

def compute_rating(obj):
   _service_ratings = 0
   _current_income = obj['service_income']
   _last_month_income = obj['service_income_last_month']
   
   if _current_income != 0:
        if _current_income >= _last_month_income:
                _increase_product = _last_month_income * 100
                _increase_percent = _increase_product / _current_income
                _service_ratings += 100 - _increase_percent
        else:
                _decrease_product = _current_income * 100
                _decrease__percent = _decrease_product / _last_month_income
                _service_ratings += 100 - _decrease__percent
   elif _current_income == 0 and _last_month_income != 0:
       _service_ratings += 100             
           
   return _service_ratings   

def load_services_sales(request):
    _services = services.objects.filter(service_status = 'active').values()
    _appointment = appointments.objects.filter(appointment_status = 'Done').values()
    _current_datetime = datetime.now()
    _current_month = _current_datetime.month
    _current_year = _current_datetime.year
    
    object_services_income = []
    
    for y in _services:
        service_id = y['id']
        service_income = 0
        service_income_last_month = 0
        
        for x in _appointment:
            _service_price = x['service_price']
            _service_id = x['service_id']
            _appointment_date = x['appointment_date']
            
            _date_parts = _appointment_date.split("-")
            _year = int(_date_parts[0])
            _month = int(_date_parts[1])
            
            if service_id == _service_id:
                if _month == _current_month and _year == _current_year:
                    service_income += _service_price
                
                if _month == 1:
                    if _year == (_current_year - 1) and _month == 12:
                        service_income_last_month += _service_price
                else:
                    if _year == _current_year and _month == (_current_month - 1):
                        service_income_last_month += _service_price
        
        income_objects = {'service_income' : service_income, 'service_income_last_month' : service_income_last_month}
        service_rating = compute_rating(income_objects)        
        
        object_services_income.append({
                                       'service_id' : service_id,
                                       'service_income' : service_income,
                                       'service_income_last_month' : service_income_last_month,
                                       'service_rating' : service_rating
                                     })
        
    context = {
        'services' : _services,
        'object_services_income' : object_services_income
    }
    
    return render(request, 'admin_dashboard_templates/services_sales.html', context)

def load_client_home_cards(request):
    client_email = request.session['email']
    client_appointments = appointments.objects.filter(client_email = client_email).values()
    count_appointment = client_appointments.count()
    _upcoming_appointments = 0
    _done_appointments = 0 
    _canceled_appointments = 0
    
    for x in client_appointments:
        _appointment_status = x['appointment_status']
        
        if _appointment_status == 'Confirmed':
            _upcoming_appointments += 1
        
        elif _appointment_status == 'Done':
            _done_appointments += 1
        
        elif _appointment_status == 'Canceled':
            _canceled_appointments += 1
    
    context = {
        'total_appointments' : count_appointment,
        'upcoming' : _upcoming_appointments,
        'done' : _done_appointments,
        'canceled' : _canceled_appointments
    }
    return render(request, 'client_home_templates/client_cards.html', context)

def load_client_home_table(request):
    _upcoming_booking = appointments.objects.filter(appointment_status = 'Confirmed', client_email = request.session['email']).values()
    _sched = employee_schedule.objects.all().values()
    _employee = authentication.objects.all().values()
    _services = services.objects.all().values()
    _booking_data = []
    
    for details in _upcoming_booking:
        _booking_id = details['id']
        
        _employee_id = ''
        
        _service_img = ''
        _service_name = ''
        _service_price = 0
        _booking_date = ''
        _booking_time = ''
        _service_assistant_name = ''
        _service_assistant_email = ''
        
        for service_details in _services:
            if service_details['id'] == details['service_id']:
                _service_img += service_details['service_img']
                _service_name += service_details['service_name']
                _service_price += service_details['service_price']
            
                for sched_details in _sched:
                    if sched_details['appointment_id'] == _booking_id:
                        _employee_id += sched_details['employee_vid']
                        _booking_date += sched_details['date']
                        _booking_time += sched_details['time']

                        for employee_details in _employee:
                            if employee_details['v_id'] == _employee_id:
                                _service_assistant_name += employee_details['first_name']+' '+employee_details['last_name']
                                _service_assistant_email += employee_details['email']            
         
        _booking_data.append({
            'img' : _service_img,
            'service_name' : _service_name,
            'price' : _service_price,
            'date' : _booking_date,
            'time' : _booking_time,
            'assistant_name' : _service_assistant_name,
            'assistant_email' : _service_assistant_email
        })  
            
    context = {
        'upcoming' : _booking_data
    }
    return render(request, 'client_home_templates/client_home_table.html', context)

#settings server sides
def logout_view(request):
    return render(request, 'navbar/logout.html')

def validate_admin_account(request):
    admin_email = request.session['email']
    admin_auth = authentication.objects.get(email = admin_email)
    
    if admin_auth.email == 'admin' or check_password('admin', admin_auth.password):
        return JsonResponse({'msg' : 'default'})
    else:
        return JsonResponse({'msg' : 'valid'})
    
def settings_view(request):
    client_settings_request = request.GET['req']
    
    if client_settings_request == 'account_settings':
        return render(request, 'settings/account_settings.html')
    
    elif client_settings_request == 'account_details':
        return render(request, 'settings/view_account_details.html')
    else:
        return render(request, 'settings/delete_account.html')

def account_update_email_notif(old_email, email):
    _v_email  = ''
    
    if email != old_email:
        html_message = render_to_string('email.html', 
                                    {'header': 'Email Updated', 
                                        'title': 'Your email was changed.',
                                        'text': 'We will send a verification code once you log in to your account'}
                                    )
        _v_email += email
        
    else: 
        html_message = render_to_string('email.html', 
                                    {'header': 'Password Updated', 
                                        'title': 'Your password was changed.',
                                        'text': 'Please log in to your account using your new password.'}
                                    )
        _v_email += old_email
        
    plain_message = strip_tags(html_message)
        
    sent_count =send_mail(
        "Orient SPA account verification Code",
        plain_message,
        settings.EMAIL_HOST_USER,
        [_v_email],
        fail_silently=False,
        html_message=html_message
        )
    return sent_count
    
#check what data does the user updated
@api_view(['POST'])    
def updateAccount(request):
    data = request.data
    
    _check_email = authentication.objects.filter(email = data['email'])
    _user_auth = authentication.objects.get(v_id = request.session['v_id'])
    _old_password = _user_auth.password
    
    if data['f_name'] == _user_auth.first_name and data['l_name'] == _user_auth.last_name and data['email'] == _user_auth.email and data['new_pass'] == '':
        return Response({'msg' : 'Nothing to update'})
    if _check_email.exists() and data['email'] != request.session['email']:
        return Response({'msg' : 'Email already exist.'})
    
    if data['new_pass'] != '' and data['new_pass'] != data['c_pass']:
        return Response({'msg' : 'Passwords dont match'})
    
    if check_password(data['new_pass'], _old_password):
        return Response({'msg' : 'You cannot use password the same with your old password'})
    
    if not check_password(data['new_pass'], _old_password) and data['new_pass'] == data['c_pass'] and data['new_pass'] != '' and data['email'] == 'admin':
        return Response({'msg' : 'Password cannot change with default email "admin". Please change your email'})
    
    if not check_password(data['new_pass'], _old_password) and data['new_pass'] == data['c_pass'] and data['new_pass'] != '':
        _user_auth.password = make_password(data['new_pass'])
        _user_auth.save()
        
        account_update_email_notif( request.session['email'] ,data['email'])
    
    _user_auth.first_name = data['f_name']
    _user_auth.last_name = data['l_name']
    _user_auth.save()
    
    if data['email'] != request.session['email']:
        _email_response = account_update_email_notif( request.session['email'] ,data['email'])
        if _email_response == 1:
            _user_auth.email = data['email']
            _user_auth.v_status = 'unverified'
            _user_auth.save()
    
        return Response({'msg' : 200})
    
    else:
        return Response({'msg' : 200})

@api_view(['POST'])
def delete_account(request):
    data = request.data
    
    _services = services.objects.all()
    _appointments = appointments.objects.all()
    _scheduled = employee_schedule.objects.all()
    _rating = ratings_comments.objects.all()
    _reply = replies_comment.objects.all()
    _user_account = authentication.objects.get(email = request.session['email'])
    
    if not check_password(data['admin_pass'], _user_account.password):
        return Response({'msg' : 'Incorrect Password.'})
    
    _user_account.delete()
    
    if request.session['priv'] == 1:
        _services.delete()
        _appointments.delete()
        _scheduled.delete()
        _rating.delete()
        _reply.delete()
        
    if request.session['priv'] == 2:
        _client_appointments = appointments.objects.filter(client_email = request.session['email'])
        if _client_appointments.exists():
            _client_appointments.delete()
        
        _client_rating  = ratings_comments.objects.filter(user_id = request.session['v_id'])
        if _client_rating.exists():
            _client_rating.delete()
    
    return Response({'msg' : 200})

@api_view(['POST'])
def send_change_pass_link(request):
    data = request.data
    user_auth = authentication.objects.get(email = data['email'])
    
    html_message = render_to_string('settings/change_pass_email.html', 
                                    {'email' : data['email'],
                                     'v_id' : user_auth.v_id}
                                        )
    plain_message = strip_tags(html_message)
        
    sent_count =send_mail(
        "Orient SPA Forgot Password Link",
        plain_message,
        settings.EMAIL_HOST_USER,
        [data['email']],
        fail_silently=False,
        html_message=html_message
        )
    if sent_count == 1:
        return Response({'msg' : 200})
    
    return Response({'msg' : 'Something went wrong.'})

@api_view(['POST'])
def update_user_password(request):
    data = request.data
    
    _user = authentication.objects.get(email = data['email'])
    _user.password = make_password(data['new_pass'])
    _user.save()
    
    return Response({'msg' : 200})

@api_view(['POST'])
def update_salary(request):
    data = request.data
    
    _emp_data = employment_data.objects.filter(employee_v_id = data['v_id'])
    
    if _emp_data.exists():
        _update_data = employment_data.objects.get(employee_v_id = data['v_id'])
        _update_data.basic_monthly_pay = data['salary']
        _update_data.save()
        return Response({'msg': 'Salary Updated!'})
    
    employment_data.objects.create(
        employee_v_id = data['v_id'],
        basic_monthly_pay = data['salary']
    )
    
    return Response({'msg': 'Salary Updated!'})