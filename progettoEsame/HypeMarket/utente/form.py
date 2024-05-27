from typing import Any
from django import forms
from .models import *
from django.contrib import messages
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit, Field, Div, Layout


class Registrazione(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['username','nome', 'cognome', 'email', 'password']

    username=forms.CharField(widget=forms.TextInput(), max_length=25)
    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    email=forms.CharField(widget=forms.EmailInput(), max_length=25)
    password=forms.CharField(widget=forms.PasswordInput(), max_length=25)
    confermaPassword=forms.CharField(widget=forms.PasswordInput(), max_length=25)
    confermaPassword.label = 'Conferma password'

    def __init__(self, *args, **kwargs):
        super(Registrazione, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-registrazione'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('nome', css_class='form-control'),
            Field('cognome', css_class='form-control'),
            Field('username', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('password', css_class='form-control'),
            Field('confermaPassword', css_class='form-control'),
            Submit('submit', 'Registrati', css_class='btn btn-primary'),
        )
    
    def save(self, commit=True):
        utente = super().save(commit=False)
        utente.set_password(self.cleaned_data['password'])
        if commit:
            utente.save()
        return utente

class Login(forms.Form):
    class Meta:
        model = Utente
        fields = ['username', 'password']

    username=forms.CharField(widget=forms.TextInput(), max_length=25)
    password=forms.CharField(widget=forms.PasswordInput(), max_length=25)

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-login'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('password', css_class='form-control'),
            Submit('submit', 'Login', css_class='btn btn-primary'),
        )

class Informazioni(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['dataNascita','pIva']

    dataNascita=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    pIva=forms.CharField(widget=forms.TextInput(), max_length=11, required=False)

    def __init__(self, *args, **kwargs):
        super(Informazioni, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-informazioni'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('dataNascita', css_class='form-control'),
            Field('pIva', css_class='form-control'),
            Submit('submit', 'Modifica', css_class='btn btn-primary'),
        )

    def save(self, commit=True, user=None):
        informazioni = super().save(commit=False)
        if user:
            user.dataNascita = informazioni.dataNascita
            user.pIva = informazioni.pIva
        if commit:
            user.save()
        return user

class Indirizzo(forms.ModelForm):

    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    via=forms.CharField(widget=forms.TextInput(), max_length=25)
    citta=forms.CharField(widget=forms.TextInput(), max_length=25)
    cap=forms.CharField(widget=forms.TextInput(), max_length=5)
    provincia=forms.CharField(widget=forms.TextInput(), max_length=2)
    nazione=CountryField().formfield()
    telefono=forms.CharField(widget=forms.TextInput(attrs={'type':'number'}), max_length=15)

    def __init__(self, *args, **kwargs):
        super(Indirizzo, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-indirizzo'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('nome', css_class='form-control'),
            Field('cognome', css_class='form-control'),
            Field('via', css_class='form-control'),
            Field('citta', css_class='form-control'),
            Field('cap', css_class='form-control'),
            Field('provincia', css_class='form-control'),
            Field('nazione', css_class='form-control'),
            Field('telefono', css_class='form-control'),
            Submit('submit', 'Registrati', css_class='btn btn-primary'),
        )
    
    def save(self, commit=True, user=None):
        indirizzo = super().save(commit=False)
        if user:
            indirizzo.utente = user
        if commit:
            indirizzo.save()
        return indirizzo

class Spedizione(Indirizzo):
    class Meta:
        model = IndirizzoSpedizione
        fields = ['nome','cognome','via', 'citta', 'cap', 'provincia', 'nazione', 'telefono']

class Fatturazione(Indirizzo):
    class Meta:
        model = IndirizzoFatturazione
        fields = ['nome','cognome','via', 'citta', 'cap', 'provincia', 'nazione', 'telefono']

class Banca(forms.ModelForm):
    class Meta:
        model = DatiBancari
        fields = ['nome','cognome','iban','banca']

    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    iban=forms.CharField(widget=forms.TextInput(), max_length=27)
    banca=forms.CharField(widget=forms.TextInput(), max_length=50)

    def __init__(self, *args, **kwargs):
        super(Banca, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-banca'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('nome', css_class='form-control'),
            Field('cognome', css_class='form-control'),
            Field('iban', css_class='form-control'),
            Field('banca', css_class='form-control'),
            Submit('submit', 'Modifica', css_class='btn btn-primary'),
        )

    def save(self, commit=True, user=None):
        banca = super().save(commit=False)
        if user:
            banca.utente = user
        if commit:
            banca.save()
        return banca

class Carta(forms.ModelForm):
    class Meta:
        model = CartaCredito
        fields = ['nome','cognome','numero','scadenzaMese','scadenzaAnno','cvv']

    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    numero=forms.CharField(widget=forms.TextInput(), max_length=16)
    scadenzaMese=forms.CharField(max_length=2)
    scadenzaMese.label = 'Mese di scadenza'
    scadenzaAnno=forms.CharField(max_length=4)
    scadenzaAnno.label = 'Anno di scadenza'
    cvv=forms.CharField(widget=forms.TextInput(), max_length=3)
    cvv.label = 'CVV'

    def __init__(self, *args, **kwargs):
        super(Carta, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-carta'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('nome', css_class='form-control'),
            Field('cognome', css_class='form-control'),
            Field('numero', css_class='form-control'),
            Field('scadenzaMese', css_class='form-control'),
            Field('scadenzaAnno', css_class='form-control'),
            Field('cvv', css_class='form-control'),
            Submit('submit', 'Modifica', css_class='btn btn-primary'),
        )

    def save(self, commit=True, user=None):
        carta = super().save(commit=False)
        if user:
            carta.utente = user
        if commit:
            carta.save()
        return carta