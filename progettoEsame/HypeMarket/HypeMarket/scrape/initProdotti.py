from prodotto.models import Prodotto, Taglia
import json
from pathlib import Path
from datetime import datetime
import locale

def eraseProdotti():
    Prodotto.objects.all().delete()
    Taglia.objects.all().delete()
    print('Database cancellato')

def initProdotti():
    i=1
    if len(Prodotto.objects.all()) == 0:
        with open(Path(__file__).with_name('db_prodotti.json'), 'r', encoding='utf-8') as f:
            scraped = json.load(f)
            for prod in scraped:
                print(i)
                locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
                data = datetime.strptime(prod['Data'], '%d %B %Y')
                p=Prodotto(titolo=prod['Titolo'], immagine=prod['Immagine'], idModello=prod['Id'], dataRilascio=data)
                p.save()
                for t in prod['Taglie']:
                    taglia=Taglia(prodotto=p,taglia=t)
                    taglia.save()
                i+=1
    print('Database inizializzato')