from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    if 'v_id' not in request.session:
        return redirect('/')
    return render(request, 'home.html')

def appointment(request):
    if 'v_id' not in request.session:
        return redirect('/')
    return render(request, 'appointment.html')

def services(request):
    if 'v_id' not in request.session:
        return redirect('/')
    return render(request, 'services.html')

def chat(request):
    if 'v_id' not in request.session:
        return redirect('/')
    return render(request, 'chat.html')

def settings(request):
    if 'v_id' not in request.session:
        return redirect('/')
    return render(request, 'settings.html')