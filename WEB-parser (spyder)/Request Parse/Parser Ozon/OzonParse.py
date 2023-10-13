import logging
import collections

import requests
from bs4 import BeautifulSoup
import csv

logging.basicConfig(level = logging.INFO )
logger = logging.getLogger('OZONE')

ParserResult = collections.namedtuple(
    'ParseResult',
    (
         'goods_name',
         'cost',
         'oldcost',
         'discount',
         'url'
    )
)

HEADERS = ( 'Наименование', 'Цена', 'Старая цена', 'Скидка', 'Ссылка')

class Parser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0', 
            'Accept-Language': 'ru',
        }
        self.result = []

        
    def load_page(self, page: int = None): #-----------СКАЧИВАЕМ СТРАНИЦУ-----------
        url = 'https://www.ozon.ru/category/kompyutery-i-komplektuyushchie-15690/'
        res = self.session.get(url = url)
        res.raise_for_status()
                
        with open('test.html', 'w') as output_file:
            output_file.write(res.text)
        
        return res.text
    
    def pars_page (self, text: str): #-----------ВЫДИРАЕМ БЛОКИ-----------
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('div.a0c6.a0d.a0c9')
        print(container.__len__())
        for block in container:
            self.parse_block(block=block)
            
    def parse_block (self, block):  

        #-----------ССЫЛКА-----------
        url_block = block.select_one('a.a0v2.a0v4.tile-hover-target')
        if not url_block:
            logger.error('no url_block')
            return
        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return
        url = 'https://www.ozon.ru' + url
        
        #-----------НАИМЕНОВАНИЕ ВЕЩИ-----------
        
        goods_name = block.select_one('a.a2g0.tile-hover-target')
        if not goods_name:
            logger.error(f'no goods_name in {url}')
            return
        goods_name=goods_name.text.strip()
        
        #-----------ЦЕНА/СКИДКА-----------
        
        cost_block = block.select_one('a.a0y9.a0z0.tile-hover-target')
        if not cost_block:
            logger.error(f'no cost_block in {url}')
            return
                
        cost = cost_block.select_one('span.b5v6.b5v7.c4v8')
        if not cost:
            logger.error(f'no cost in {url}')
            return
        cost=cost.text.strip()
        
        oldcost = cost_block.select_one('span.b5v9.b5v7')
        if not oldcost:
            logger.error(f'no oldcost in {url}')
            return
        oldcost=oldcost.text.strip()
        
        discount = cost_block.select_one('div.a0x.a5d2.item')
        if not discount:
            logger.error(f'no discount in {url}')
            return
        discount=discount.text.strip()

        
        #-----------ЗАПОЛНЕНИЕ ВЫВОДА-----------
        self.result.append(ParserResult(
            goods_name=goods_name,
            cost=cost,
            oldcost=oldcost,
            discount=discount,
            url=url
        ))
        
        #logger.debug('%s, %s, %s, %s', url, goods_name, cost, oldcost, discount)
        #logger.debug('-' * 90)
    
    def save_result(self):
        path = './result_OZON.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL )
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)
            
    def run (self):
        text = self.load_page()
        self.pars_page(text=text)
        logger.info(f' получили {len(self.result)} товара')
        self.save_result()
        
if __name__ == '__main__':
    parser = Parser()
    parser.run()
    
