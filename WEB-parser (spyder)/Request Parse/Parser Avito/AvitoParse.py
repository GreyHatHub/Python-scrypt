import logging
import collections

import requests
from bs4 import BeautifulSoup
import csv

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('AVITO')

ParserResult = collections.namedtuple(
    'ParseResult',
    (
         'foto_url',    
         'brand_name',
         'goods_name',
         'cost',
         'oldcost',
         'mesto',
         'url'
    )
)

HEADERS = ( 'Наименование', 'Описание', 'Цена', 'Старая цена', 'Местоположение', 'Ссылка')

class Parser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0', 
            'Accept-Language': 'ru',
        }
        self.result = []
    
    def page_counter(self, page: int = None):
        urka = 'https://www.avito.ru/rossiya/avtomobili/bmw/x5'
        res = self.session.get(url = urka)
        soup = BeautifulSoup(res.text, 'lxml')
        container = soup.select('span.pagination-item-1WyVp')
        return container[-2].text
        
    #-----------ЗАГРУЗКА_СТРАНИЦЫ-----------   
    def load_page(self, text: str, page: int = None):
        url = 'https://www.avito.ru/rossiya/avtomobili/bmw/x5?p='+text
        res = self.session.get(url = url)
        res.raise_for_status()
        return res.text
    
    #-----------ПАРСИНГ_НАГРУЗКИ_ЗАГРУЖЕННОЙ_СТРАНИЦЫ-----------   
    def pars_page (self, text: str):
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('div.iva-item-content-m2FiN') #ПОИСК ТЭГОВ
        for block in container:
            self.parse_block(block=block)
            
    def parse_block (self, block):  
        
        #-----------ССЫЛКА-----------
        url_block = block.select_one('a.link-link-39EVK')
        if not url_block:
            logger.error('no url_block')
            return
        
        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return
        url = 'https://www.avito.ru' + url
        
        #-----------ССЫЛКА НА ФОТО-----------
        foto_blocks = block.select_one('div.photo-slider-root-1w2KO')
        if not foto_blocks:
            logger.error('no foto_block')
            return
        
        #foto_block = foto_blocks.select_one('img.photo-slider-image-1fpZZ')
        foto_block = foto_blocks.select_one('li')
        if not foto_block:
            foto_url=""
        else:
            foto_url=foto_block['data-marker']
            foto_url=foto_url.replace('slider-image/image-','')
            foto_url=f'<img src=\"{foto_url}\">'
                    
        #-----------ЦЕНА/СКИДКА-----------
        
        cost = block.select_one('span.price-text-1HrJ_')
        if not cost:
            logger.error(f'no cost_block in {url}')
            return
        cost=cost.text.strip()
        
        oldcost = block.select_one('span.price-noaccent-rl2hZ')
        if not oldcost:
            oldcost='-'
        else:
            oldcost=oldcost.text.strip()        
        
        #-----------НАИМЕНОВАНИЕ БРЭНДА-----------
        
        brand_name = block.select_one('h3.title-root-395AQ')
        if not brand_name:
            logger.error(f'no brand_name in {url}')
            return
        brand_name=brand_name.text.strip()
        
        #-----------НАИМЕНОВАНИЕ ВЕЩИ-----------
        
        goods_name = block.select_one('div.iva-item-text-2xkfp')
        if not goods_name:
            logger.error(f'no goods_name in {url}')
            return
        goods_name=goods_name.text.strip()
        
        #-----------МЕСТОПОЛОЖЕНИЕ-----------
        
        mesto = block.select_one('span.geo-address-9QndR')
        if not mesto:
            logger.error(f'no goods_name in {url}')
            return
        
        mesto=mesto.text.strip()        
        
        #-----------ЗАПОЛНЕНИЕ ВЫВОДА-----------
        self.result.append(ParserResult(
            foto_url=foto_url,       #ссылка на фото
            brand_name=brand_name,  #Имя
            goods_name=goods_name,  #описание
            cost=cost,              #цена
            oldcost=oldcost,        #старая цена
            mesto=mesto,            #местоположение
            url=url                 #ссылка
        ))
        
        logger.debug('%s, %s, %s, %s, %s, %s', url, brand_name, goods_name, mesto, cost, oldcost)
        logger.debug('-' * 90)
        
    #-----------СОХРАНЕНИЕ ТАБЛИЦЫ CSV-----------
    def save_result(self):
        path = './result_AVITO.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL )
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)
                
    #-----------СОХРАНЕНИЕ ТАБЛИЦЫ HTML-----------           
    def html_table(self):
        html = """<HTML>
        <style>
            table {1} 
                font-size: 10pt;
            {2}
        </style>
        <body>
            <h1>Scraping AVITO</h1>
            <table border="3" width="100%" cellpadding="4">
                {0}
            </table>
        </body>
        </HTML>"""
        tr = "<tr>{0}</tr>"
        td = "<td>{0}</td>"
        href="<a href=\"{0}\">"
        subitems = [tr.format(''.join([td.format(href.format(item[-1]) + item[i]) for i in range(len(item)-1)])) for item in self.result]
           
        display = open("result_AVITO.html", 'w')
        display.write(html.format("".join(subitems),'{','}'))
    
    #-----------ВЫЗОВ функций-----------
    def run (self):
        counter = self.page_counter()
        logger.info(f' всего страниц {counter} ')
        for i in range(1,int(counter)):
            text = self.load_page(text=str(i))
            logger.info(f' Страница {i} загружена')
            self.pars_page(text=text)
            logger.info(f' Страница {i} Обработана')
            logger.info('-'*50)
        logger.info(f' получили {len(self.result)} товара')
        self.save_result()
        self.html_table()

#-----------ЗАПУСК-----------        
if __name__ == '__main__':
    parser = Parser()
    parser.run()