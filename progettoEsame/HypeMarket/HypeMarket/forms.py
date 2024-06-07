from django import forms
from utente.models import *
from prodotto.models import *
from gestione.models import *
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit, Field, Layout
from datetime import datetime as time
import os
from django.conf import settings

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
        fields = ['immagineProfilo','dataNascita','pIva']

    dataNascita=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    dataNascita.label = 'Data di nascita'
    pIva=forms.CharField(widget=forms.TextInput(), max_length=11, required=False)
    pIva.label = 'Numero partita IVA'
    immagineProfilo = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}), required=False)
    immagineProfilo.label = 'Immagine del profilo'

    def __init__(self, *args, **kwargs):
        super(Informazioni, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-informazioni'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('immagineProfilo', css_class='form-control'),
            Field('dataNascita', css_class='form-control'),
            Field('pIva', css_class='form-control'),
            Submit('submit', 'Modifica', css_class='btn btn-primary'),
        )

    def save(self, commit=True, utente=None):
        informazioni = super().save(commit=False)
        if utente:
            immagine = informazioni.immagineProfilo
            if immagine and utente.immagineProfilo:
                if os.path.exists(utente.immagineProfilo.path):
                    os.remove(utente.immagineProfilo.path)
            if immagine:
                destinazione = os.path.join(settings.MEDIA_ROOT,'immaginiProfilo', utente.username)
                os.makedirs(destinazione, exist_ok=True)
                nome = immagine.name
                path = os.path.join(destinazione, nome)
                with open(path, 'wb+') as f:
                    for chunk in immagine.chunks():
                        f.write(chunk)
                utente.immagineProfilo = os.path.join('immaginiProfilo', utente.username, nome)
            if informazioni.dataNascita:
                utente.dataNascita = informazioni.dataNascita
            if informazioni.pIva:
                utente.pIva = informazioni.pIva
        if commit:
            utente.save()
        return utente

class Indirizzo(forms.ModelForm):

    nome=forms.CharField(widget=forms.TextInput(), max_length=25)
    cognome=forms.CharField(widget=forms.TextInput(), max_length=25)
    via=forms.CharField(widget=forms.TextInput(), max_length=25)
    citta=forms.CharField(widget=forms.TextInput(), max_length=25)
    cap=forms.CharField(widget=forms.TextInput(), max_length=5)
    provincia=forms.CharField(widget=forms.TextInput(), max_length=2)
    nazione=CountryField().formfield()
    telefono=forms.CharField(widget=forms.TextInput(attrs={'type':'number'}), max_length=10)

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
    
    def save(self, commit=True, utente=None):
        indirizzo = super().save(commit=False)
        if utente:
            indirizzo.utente = utente
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

    def save(self, commit=True, utente=None):
        banca = super().save(commit=False)
        if utente:
            banca.utente = utente
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

    def save(self, commit=True, utente=None):
        carta = super().save(commit=False)
        if utente:
            carta.utente = utente
        if commit:
            carta.save()
        return carta

class PropostaOfferta(forms.ModelForm):

    prezzo=forms.FloatField(widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(PropostaOfferta, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-propostaofferta'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Field('prezzo', css_class='form-control'),
            Submit('submit', 'Registrati', css_class='btn btn-primary'),
        )

class OffertaForm(PropostaOfferta):
    
    class Meta:
        model = Offerta
        fields = ['prezzo']
    
    def save(self, commit=True, utente=None, prodotto=None, taglia=None, indirizzoSpedizione=None, carta=None):
        offerta = super().save(commit=False)
        if utente:
            offerta.taglia = taglia
            offerta.utente = utente
            offerta.prodotto = prodotto
            offerta.data = time.now().date()
            offerta.indirizzoSpedizione = indirizzoSpedizione
            offerta.carta = carta
        if commit:
            offerta.save()
        return offerta
    
class PropostaForm(PropostaOfferta):
    
    class Meta:
        model = Proposta
        fields = ['prezzo']
    
    def save(self, commit=True, utente=None, prodotto=None, taglia=None, indirizzoFatturazione=None, banca=None):
        proposta = super().save(commit=False)
        if utente:
            proposta.taglia = taglia
            proposta.utente = utente
            proposta.prodotto = prodotto
            proposta.data=time.now().date()
            proposta.indirizzoFatturazione= indirizzoFatturazione
            proposta.banca= banca
        if commit:
            proposta.save()
        return proposta
    
class AcquistoVendita(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AcquistoVendita, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_id = 'form-vendita'
        helper.form_method = 'POST'
        helper.layout = Layout(
            Submit('submit', 'Vendi', css_class='btn btn-primary'),
    )

class VenditaForm(AcquistoVendita):
    class Meta:
        model = Vendita
        fields = []
    
    def save(self, commit=True, utente=None, prodotto=None, taglia=None, prezzo=None, indirizzoFatturazione=None, banca=None):
        vendita = super().save(commit=False)
        if utente:
            vendita.taglia = taglia
            vendita.utente = utente
            vendita.prodotto = prodotto
            vendita.data=time.now().date()
            vendita.prezzo=prezzo
            vendita.indirizzoFatturazione= indirizzoFatturazione
            vendita.banca= banca
        if commit:
            vendita.save()
        return vendita
    
class AcquistoForm(AcquistoVendita):
    class Meta:
        model = Acquisto
        fields = []
    
    def save(self, commit=True, utente=None, prodotto=None, taglia=None, prezzo=None, indirizzoSpedizione=None, carta=None):
        acquisto = super().save(commit=False)
        if utente:
            acquisto.taglia = taglia
            acquisto.utente = utente
            acquisto.prodotto = prodotto
            acquisto.data=time.now().date()
            acquisto.prezzo=prezzo
            acquisto.indirizzoSpedizione= indirizzoSpedizione
            acquisto.carta= carta
        if commit:
            acquisto.save()
        return acquisto

class Cerca(forms.Form):
    
    stringa=forms.CharField(widget=forms.TextInput(attrs={'class': 'pulsanti'}), max_length=25)
    stringa.label = ''

    def __init__(self, *args, **kwargs):
        super(Cerca, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_show_labels = False
        helper.form_id = 'form-cerca'
        helper.layout = Layout(
            Field('stringa', css_class='form-control', placeholder='Cerca'),
            Submit('submit', 'Cerca', css_class='btn btn-primary'),
        )

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['voto','testo']

    voto = forms.ChoiceField(widget=forms.Select(attrs={'class': 'voto'}), choices=[(i, ('★' * i)) for i in range(1, 6)])
    voto.label = 'Inserire un voto da 1 a 5'
    testo=forms.CharField(widget=forms.Textarea(attrs={'class': 'testo'}), max_length=400)
    testo.label = 'Inserire un breve commento'
    
    def __init__(self, *args, **kwargs):
        super(RecensioneForm, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_show_labels = False
        helper.form_id = 'form-cerca'
        helper.layout = Layout(
            Field('voto', css_class='form-control'),
            Field('testo', css_class='form-control'),
            Submit('submit', 'Cerca', css_class='btn btn-primary'),
        )

    def save(self, commit=True, acquisto=None):
        recensione = super().save(commit=False)
        if acquisto:
            recensione.acquisto = acquisto
        if commit:
            recensione.save()
        return recensione