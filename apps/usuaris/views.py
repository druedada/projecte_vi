from axes.helpers import get_lockout_message
from axes.handlers.proxy import AxesProxyHandler
from .forms import UserRegisterForm, UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
	context = {
		'app_title': 'Usuaris'
	}
	return render(request, 'base.html', context)


def registre(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticación e inicio de sesión automático
            from django.contrib.auth import authenticate, login
            correu = form.cleaned_data['correu'].strip().lower()
            contrasenya = form.cleaned_data['contrasenya1']
            user = authenticate(request, username=correu, password=contrasenya)
            if user is not None:
                login(request, user)
            return redirect('usuaris:index')  # Redirige tras registro correcto
    else:
        form = UserRegisterForm()
    return render(request, 'usuaris/registre.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            correu = form.cleaned_data['correu'].strip().lower()
            contrasenya = form.cleaned_data['contrasenya']
            # Comprobar si el usuario está bloqueado por Axes
            if AxesProxyHandler.is_locked(request, credentials={'username': correu}):
                error = get_lockout_message()
            else:
                try:
                    user_obj = User.objects.get(email=correu)
                    username = user_obj.username
                except User.DoesNotExist:
                    username = correu  # fallback por si username==email
                user = authenticate(request, username=username, password=contrasenya)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error = 'Correu o contrasenya incorrectes.'
    else:
        form = UserLoginForm()
    return render(request, 'usuaris/login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')