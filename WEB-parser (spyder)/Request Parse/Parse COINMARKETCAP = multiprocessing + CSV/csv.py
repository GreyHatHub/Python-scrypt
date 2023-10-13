from multiprocessing import Pool
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('tbody').find_all('tr')
    links = []
    for td in tds:
        a = td.find('a', class_='cmc-link').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links


def text_before_word(text, word):
    line = text.split(word)[0].strip()
    return line


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = text_before_word(soup.find('h2', class_='sc-fzqBZW bQqdJy h1___3QSYG').text)
    except:
        name = ''
    try:
        price = text_before_word(soup.find('div', class_='priceValue___11gHJ').text)
    except:
        price = ''
    data = {'name': name,
            'price': price}
    #print(f'{name} и {price}')
    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], data['price'])


def make_all(link):
    html = get_html(link)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all'
    all_links = get_all_links(get_html(url))

    with Pool(1) as p:
        p.map(make_all, all_links)

    
    end = datetime.now()
    total = end - start
    print(str(total))
    a = input()


if __name__ == '__main__':
     main()
