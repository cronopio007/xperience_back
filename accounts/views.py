from django.shortcuts import render, redirect
from .forms import RegistrationForm

from .models import Account
from django.contrib import messages, auth

# Create your views here.

## crear funciones de login y logout

def register(request):
    ## request Post contiene todos los valores de fields
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # si tiene todos los fields requeridos  se corre lo siguiente
        if form.is_valid():
            ## limpiar los valores despues de enviarlos
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_name = email.split("@")[0]
            user = Account.objects.create_user(first_name= first_name,
                                                last_name = last_name, 
                                                email = email, 
                                                user_name =user_name, 
                                                password= password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'registro exitoso')
            return redirect('register')
    else:

        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request,  'accounts/register.html', context)



def login(request):
    if request.method =='POST':
        ## son los nombres q se le dio en el login.html
        email = request.POST['email']
        password = request.POST['password']

        user = auth(email = email, password = password)

        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'estan logeado')
            return redirect('home')
        else:
            messages.error(request, 'credenciales incorrectas')
            return redirect('login')

    return render(request, 'accounts/login.html')



def logout(request):

    return render(request, 'accounts/logout.html')