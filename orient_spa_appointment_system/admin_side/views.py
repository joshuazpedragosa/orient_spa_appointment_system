from django.shortcuts import render, redirect

# Create your views here.
def admin_dashboard(request):
    if 'v_id' not in request.session or request.session['priv'] != 1:
        return redirect('/')
    
    return render(request, 'admin_dashboard.html')

def admin_employee(request):
    if 'v_id' not in request.session or request.session['priv'] != 1:
        return redirect('/')
    
    return render(request, 'add_employee.html')