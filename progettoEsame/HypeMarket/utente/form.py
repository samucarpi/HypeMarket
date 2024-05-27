from typing import Any
from django import forms
from .models import *
from django.contrib import messages
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit, Field, Div, Layout

class FormRegistrazione(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['nome', 'cognome', 'email', 'password']

    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    email=forms.CharField(widget=forms.EmailInput(), max_length=25)
    password=forms.CharField(widget=forms.PasswordInput(), max_length=25)
    confermaPassword=forms.CharField(widget=forms.PasswordInput(), max_length=25)
    confermaPassword.label = 'Conferma password'

    def __init__(self, *args, **kwargs):
        super(FormRegistrazione, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-registrazione'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('nome', css_class='form-control'),
            Field('cognome', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('password', css_class='form-control'),
            Field('confermaPassword', css_class='form-control'),
            Submit('submit', 'Registrati', css_class='btn btn-primary'),
        )

class FormLogin(forms.ModelForm):
    class Meta:
        model = Utente
        fields = ['email', 'password']

    email=forms.CharField(widget=forms.EmailInput(), max_length=25)
    password=forms.CharField(widget=forms.PasswordInput(), max_length=25)

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-login'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('email', css_class='form-control'),
            Field('password', css_class='form-control'),
            Submit('submit', 'Login', css_class='btn btn-primary'),
        )

class FormModificaIndirizzo(forms.ModelForm):

    class Meta:
        model = IndirizzoSpedizione
        fields = ['nome','cognome','via', 'citta', 'cap', 'provincia', 'nazione', 'telefono']

    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    via=forms.CharField(widget=forms.TextInput(), max_length=25)
    citta=forms.CharField(widget=forms.TextInput(), max_length=25)
    cap=forms.CharField(widget=forms.TextInput(), max_length=5)
    provincia=forms.CharField(widget=forms.TextInput(), max_length=2)
    nazione=forms.CharField(widget=forms.TextInput(), max_length=25)
    telefono=forms.CharField(widget=forms.TextInput(), max_length=15)

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', IndirizzoSpedizione)
        super(FormModificaIndirizzo, self).__init__(*args, **kwargs)
        self._meta.model = self.model
        helper = FormHelper()
        helper.form_id = 'form-modificaIndirizzo'
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