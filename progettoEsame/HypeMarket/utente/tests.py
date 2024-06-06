from django.test import TestCase, Client
from django.urls import reverse
from .models import Utente,Wishlist
from prodotto.models import Prodotto

class RegistrazioneFormTest(TestCase):
    
    #inizializzazione del client
    def setup(self):
        self.client = Client()

    #test per la registrazione di un utente con le 2 password uguali
    def testRegistrazioneCorretta(self):
        datiForm = {
            'username': 'utenteTest',
            'nome': 'Utente',
            'cognome': 'Test',
            'email': 'utente@utente.test',
            'password': 'password',
            'confermaPassword': 'password',
        }
        #invio i dati del form
        response = self.client.post(reverse('utente:Registrazione'), data=datiForm)
        #controllo se l'utente è stato creato e se la pagina di reindirizzamento è corretta
        self.assertTrue(Utente.objects.filter(username='utenteTest').exists())
        self.assertRedirects(response, reverse('utente:Login'))

    #test per la registrazione di un utente con le 2 password diverse
    def testRegistrazionePasswordDiverse(self):
        datiForm = {
            'username': 'utenteTest',
            'nome': 'Utente',
            'cognome': 'Test',
            'email': 'utente@utente.test',
            'password': 'password',
            'confermaPassword': '1234567',
        }
        #invio i dati del form
        response = self.client.post(reverse('utente:Registrazione'), data=datiForm)
        #controllo se l'utente è stato creato e se sono presenti messaggi di errore
        self.assertFalse(Utente.objects.filter(username='testuser').exists())
        self.assertIn('Password non corrispondenti', [msg.message for msg in response.context['messages']])

class WishlistTestCase(TestCase):

    #inizializzazione con la creazione di un utente, di 2 prodotti e di una wishlist con i 2 prodotti
    def setUp(self):
        self.client = Client()
        self.utente = Utente.objects.create_user(username='utenteTest', email='utente@utente.test', nome='utente', cognome='test', password='12345')
        self.prodotto1 = Prodotto.objects.create(idModello='HQ1234', immagine='test1.png',titolo='Scarpe Adidas', dataRilascio='2021-04-24')
        self.prodotto2 = Prodotto.objects.create(idModello='HQ1235', immagine='test2.png',titolo='Scarpe Nike', dataRilascio='2021-04-25')
        self.wishlist = Wishlist.objects.create(utente=self.utente)
        self.wishlist.prodotti.add(self.prodotto1, self.prodotto2)

    #test per la visualizzazione della wishlist
    def testViewWishlist(self):
        #login dell'utente
        self.client.login(username='utenteTest', password='12345')
        #richiesta della pagina della wishlist
        response = self.client.get(reverse('utente:Wishlist'))
        #controllo se la pagina è stata caricata correttamente e se i prodotti sono presenti nella lista
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.prodotto1, response.context['prodotti'])
        self.assertIn(self.prodotto2, response.context['prodotti'])