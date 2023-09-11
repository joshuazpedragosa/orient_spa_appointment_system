from django.shortcuts import render, redirect
from controller.models import authentication
from django.contrib.auth.hashers import make_password
import uuid

# Create your views here.
def index(request):
    unique_id = uuid.uuid4()
    check_admin_account = authentication.objects.filter(priv = 1)
    
    if not check_admin_account.exists():
        authentication.objects.create(
            v_id = unique_id,
            priv = 1,
            first_name = 'Orient SPA',
            last_name = 'Admin',
            email = 'admin',
            password = make_password('admin'),
            random_code = 1,
            v_status = 'verified'
            
        )
    
    if 'v_id' in request.session:
        return redirect('/client_view/')
    return render (request, 'landing_page.html')

def auth(request):
    if 'v_id' in request.session:
        return redirect('/client_view/')
    return render(request, 'auth.html')

def veification(request):
    email = request.GET['email']
    return render(request, 'verification_code.html', {'email' : email})

def validate_priv(request):
    if request.session['priv'] == 1:
        return redirect('/admin_side/admin_dashboard/')
    elif request.session['priv'] == 2:
        return redirect('/home/')
    elif request.session['priv'] == 3:
        return redirect('/employee/employee_home/')
    
    return redirect('/')