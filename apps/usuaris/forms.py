
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django import forms
import re


from .models import Adreces, UsuariDireccio

class UserRegisterForm(forms.ModelForm):
    nom = forms.CharField(label="Nom")
    cognom1 = forms.CharField(label="Primer cognom")
    cognom2 = forms.CharField(label="Segon cognom", required=False)
    correu = forms.EmailField(label="Correu electrònic")
    contrasenya1 = forms.CharField(label="Contrasenya", widget=forms.PasswordInput, min_length=8, max_length=128)
    contrasenya2 = forms.CharField(label="Repeteix la contrasenya", widget=forms.PasswordInput, min_length=8, max_length=128)


    class Meta:
        model = User
        fields = ["nom", "cognom1", "cognom2", "correu", "contrasenya1", "contrasenya2"]

    def clean_contrasenya1(self):
        contrasenya = self.cleaned_data.get("contrasenya1")
        if contrasenya and len(contrasenya) < 8:
            raise ValidationError("La contrasenya ha de tenir almenys 8 caràcters.")
        if contrasenya and len(contrasenya) > 128:
            raise ValidationError("La contrasenya no pot tenir més de 128 caràcters.")
        return contrasenya

    def clean_contrasenya2(self):
        password1 = self.cleaned_data.get("contrasenya1")
        password2 = self.cleaned_data.get("contrasenya2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les contrasenyes no coincideixen.")
        if password2 and len(password2) < 8:
            raise ValidationError("La contrasenya ha de tenir almenys 8 caràcters.")
        if password2 and len(password2) > 128:
            raise ValidationError("La contrasenya no pot tenir més de 128 caràcters.")
        return password2

    def clean_nom(self):
        nom = self.cleaned_data.get("nom")
        if not nom or not nom.strip():
            raise ValidationError("El nom no pot estar buit.")
        if re.search(r'[^a-zA-ZÀ-ÿ0-9\s]', nom):
            raise ValidationError("El nom no pot contenir caràcters especials.")
        return nom

    def clean_cognom1(self):
        cognom1 = self.cleaned_data.get("cognom1")
        if not cognom1 or not cognom1.strip():
            raise ValidationError("El primer cognom no pot estar buit.")
        if re.search(r'[^a-zA-ZÀ-ÿ0-9\s]', cognom1):
            raise ValidationError("El primer cognom no pot contenir caràcters especials.")
        return cognom1

    def clean_cognom2(self):
        cognom2 = self.cleaned_data.get("cognom2")
        if cognom2 and re.search(r'[^a-zA-ZÀ-ÿ0-9\s]', cognom2):
            raise ValidationError("El segon cognom no pot contenir caràcters especials.")
        return cognom2

    def clean_correu(self):
        correu = self.cleaned_data.get("correu")
        if not re.match(r'^[^\s@]+@[a-zA-Z]+\.[a-zA-Z]+$', correu):
            raise ValidationError("El correu no és vàlid.")
        if re.search(r'[^a-zA-Z0-9@._\-]', correu):
            raise ValidationError("El correu no pot contenir caràcters especials fora de @, punt, guió i guió baix.")
        # Comprobar si ya existe un usuario con ese correo (username)
        if User.objects.filter(username=correu.strip().lower()).exists():
            raise ValidationError("Ja existeix un usuari amb aquest correu electrònic.")
        return correu

    def save(self, commit=True):
        user = super().save(commit=False)

        correu = self.cleaned_data["correu"].strip().lower()
        cognom2 = self.cleaned_data["cognom2"].strip().lower() if self.cleaned_data["cognom2"] else ""

        user.username = correu
        user.email = correu
        user.first_name = self.cleaned_data["nom"].strip().lower()
        user.last_name = f'{self.cleaned_data["cognom1"].strip().lower()} {cognom2}'.strip()
        user.set_password(self.cleaned_data["contrasenya1"])

        if commit:
            user.save()

        return user



class UserLoginForm(forms.Form):
    correu = forms.EmailField(label="Correu electrònic")
    contrasenya = forms.CharField(label="Contrasenya", widget=forms.PasswordInput, min_length=8, max_length=128)

class AdressForm(forms.ModelForm):
    poblacio = forms.CharField(label="Població")
    cp = forms.CharField(label="Codi Postal")
    carrer = forms.CharField(label="Carrer")
    numero = forms.CharField(label="Número")

    class Meta:
        model = Adreces
        fields = ["poblacio","cp",  "carrer", "numero"]

    def validate_unique(self):
        # Permetem reutilitzar adreces existents; la deduplicació es fa al save()
        # amb get_or_create i la vinculació usuari-adreça amb UsuariDireccio.
        return

    def clean_poblacio(self):
        poblacio = self.cleaned_data.get("poblacio")
        if not poblacio or not poblacio.strip():
            raise ValidationError("La població no pot estar buida.")
        if re.search(r'[^a-zA-ZÀ-ÿ0-9\s]', poblacio):
            raise ValidationError("La població no pot contenir caràcters especials.")
        return poblacio

    def clean_cp(self):
        cp = self.cleaned_data.get("cp")
        if not re.match(r'^\d{5}$', cp):
            raise ValidationError("El codi postal ha de tenir 5 dígits.")
        return cp
    
    def clean_carrer(self):
        carrer = self.cleaned_data.get("carrer")
        if not carrer or not carrer.strip():
            raise ValidationError("El carrer no pot estar buit.")
        if re.search(r'[^a-zA-ZÀ-ÿ0-9\s]', carrer):
            raise ValidationError("El carrer no pot contenir caràcters especials.")
        return carrer

    def clean_numero(self):
        numero = self.cleaned_data.get("numero")
        if not numero or not numero.strip():
            raise ValidationError("El número no pot estar buit.")
        if re.search(r'[^a-zA-Z0-9\s]', numero):
            raise ValidationError("El número no pot contenir caràcters especials.")
        return numero
    
    def save(self, user, commit=True):
        if user is None:
            raise ValueError("Cal indicar un usuari per vincular l'adreça.")

        clients, _ = Group.objects.get_or_create(name="Clients")
        user.groups.add(clients)

        direccio, _ = Adreces.objects.get_or_create(
            cp=self.cleaned_data["cp"].strip().lower(),
            poblacio=self.cleaned_data["poblacio"].strip().lower(),
            carrer=self.cleaned_data["carrer"].strip().lower(),
            numero=self.cleaned_data["numero"].strip().lower(),
        )

        if commit:
            UsuariDireccio.objects.get_or_create(user=user, direccio=direccio)

        return direccio
