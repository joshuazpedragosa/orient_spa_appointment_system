from django.shortcuts import render, redirect

# Create your views here.
def index(request):
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