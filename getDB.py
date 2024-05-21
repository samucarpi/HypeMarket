import requests
from bs4 import BeautifulSoup
import json

jsonList=[]

with open('db.json', 'w', encoding='utf-8') as f:
    page=1
    base_url=requests.get('https://hypeboost.com/it/categoria/sneakers?'+str(page))
    for i in range(0,134):
        print(page)
        soup = BeautifulSoup(base_url.content, 'html.parser')
        for prod in soup.find_all("div", {'class':'grid_item'}):
            titolo = prod.find('h3').getText()
            img = prod.find('img').get('src')
            link = prod.find('a').get('href')
            url_scarpa = requests.get(str(link))
            soup = BeautifulSoup(url_scarpa.content, 'html.parser')
            id = soup.find('table', {'class':'table table-sm mb-0'}).getText().split('\n')[8]
            data_rilascio = soup.find('table', {'class':'table table-sm mb-0'}).getText().split('\n')[17]
            taglie = []
            for taglia in soup.find_all('div', {'class':'label'}):
                taglie.append(taglia.getText())

            jsonList.append({ 'Titolo' : str(titolo), 'Immagine' : str(img), 'Id' : str(id), 'Data' : str(data_rilascio),'Taglie' : list(taglie) })

        page+=1

    json.dump(jsonList,f,ensure_ascii=False)