import requests
from bs4 import BeautifulSoup
import json
scarpe=[]
taglie=[]
json_string=[]
with open('db.json', 'w', encoding='utf-8') as f:
    p=1
    url=requests.get('https://hypeboost.com/it/categoria/sneakers?'+str(p))
    for _ in range(135):
        soup = BeautifulSoup(url.content, 'html.parser')
        scarpe = soup.find_all("div", {'class':'grid_item'})
        for prod in scarpe:
            img = prod.find('img').get('src')
            titolo = prod.find('h3').getText()
            taglie=[]
            link=prod.find('a').get('href')
            url_scarpa=requests.get(str(link))
            soup = BeautifulSoup(url_scarpa.content, 'html.parser')
            id=soup.find('table', {'class':'table table-sm mb-0'}).getText().split('\n')[8]
            data_rilascio=soup.find('table', {'class':'table table-sm mb-0'}).getText().split('\n')[17]
            taglieNonFormattate=soup.find_all('div', {'class':'label'})
            for taglia in taglieNonFormattate:
                taglie.append(taglia.getText())
            json_string.append({ 'Titolo' : str(titolo), 'Immagine' : str(img), 'Id' : str(id), 'Data' : str(data_rilascio),'Taglie' : list(taglie) })
        p+=1
    json.dump(json_string, f, ensure_ascii=False)