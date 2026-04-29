from axes.helpers import get_lockout_message
from axes.handlers.proxy import AxesProxyHandler
from .forms import AdressForm, UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
	context = {
		'app_title': 'Usuaris'
	}
	return render(request, 'base.html', context)


def registre(request):
    form = UserRegisterForm() # Instància el formulari buit per defecte
    if request.method == 'POST': # Si s'ha enviat el formulari
        form = UserRegisterForm(request.POST) # Crea el formulari amb les dades rebudes
        if form.is_valid(): # Si el formulari és vàlid
            user = form.save() # Guarda el usuari
            # Autenticació i inici de sessió automàtic
            from django.contrib.auth import authenticate, login
            correu = form.cleaned_data['correu'].strip().lower()
            contrasenya = form.cleaned_data['contrasenya1']
            user = authenticate(request, username=correu, password=contrasenya) # Autentica l'usuari
            if user is not None:
                login(request, user)
            return redirect('home')  # Redirigeix després del registre correcte

    return render(request, 'usuaris/registre.html', {'form': form})

def login_view(request):
    error = None # Missatges externs al formulari (Axes)
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            correu = form.cleaned_data['correu'].strip().lower()
            contrasenya = form.cleaned_data['contrasenya']
            # Determinar username real per a django-axes (buscar per email)
            try:
                user_obj = User.objects.get(email=correu) 
                username = user_obj.username # Utilitzar el username real per coincidir amb authenticate() i checks de Axes
            except User.DoesNotExist:
                username = correu  # fallback per si username==email 
            # Comprobar si l'usuari està bloquejat per Axes (utilitzar username real)
            if AxesProxyHandler.is_locked(request, credentials={'username': username}):
                error = get_lockout_message()
            else:
                user = authenticate(request, username=username, password=contrasenya)
                if user is not None:
                    login(request, user)
                    if user.is_staff or user.is_superuser or user.groups.filter(name='Gestor').exists():
                        return redirect('gestio:vins')
                    return redirect('home')
                else:
                    error = 'Correu o contrasenya incorrectes.'

    return render(request, 'usuaris/login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def direccio(request):
    form = AdressForm()
    if request.method == 'POST':
        form = AdressForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('usuaris:index')
            
    return render(request, 'usuaris/direccio.html', {'form': form})

def custom_lockout_view(request, credentials=None):
    form = UserLoginForm()
    error = get_lockout_message()
    return render(request, 'usuaris/login.html', {'form': form, 'error': error})