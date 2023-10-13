import requests
import fake_useragent
from bs4 import BeautifulSoup,SoupStrainer

user = fake_useragent.UserAgent().random
Header = {'User-Agent': user}

link = "https://www.avito.ru/rossiya/avtomobili/bmw/x5"
responce = requests.get(link, headers = Header).text
soup = BeautifulSoup(responce, 'lxml')

block = soup.find('div', class_='items-items-38oUm')

links = block.find_all('div', class_='iva-item-root-G3n7v photo-slider-slider-3tEix iva-item-list-2_PpT items-item-1Hoqq items-listItem-11orH js-catalog-item-enum')

for index, link in enumerate(links):
    url = link.find('a', class_='link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc').get('href')
    print( str(index+1) +'. '+url)
