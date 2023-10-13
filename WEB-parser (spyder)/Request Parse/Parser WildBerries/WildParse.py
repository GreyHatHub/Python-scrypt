import logging
import collections

import requests
from bs4 import BeautifulSoup
import csv

logging.basicConfig(level = logging.INFO )
logger = logging.getLogger('WildBerries')

ParserResult = collections.namedtuple(
    'ParseResult',
    (
         'brand_name',
         'goods_name',
         'cost',
         'oldcost',
         'discount',
         'url'
    )
)

HEADERS = ( 'Брэнд', 'Наименование', 'Цена', 'Старая цена', 'Скидка', 'Ссылка')

class Parser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0', 
            'Accept-Language': 'ru',
        }
        self.result = []

        
    def load_page(self, page: int = None):
        url = 'https://www.wildberries.ru/catalog/elektronika/tehnika-dlya-doma'
        res = self.session.get(url = url)
        res.raise_for_status()
        return res.text
    
    def pars_page (self, text: str):
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('div.dtList.i-dtList.j-card-item')
        for block in container:
            self.parse_block(block=block)
            
    def parse_block (self, block):  
        
        #-----------ССЫЛКА-----------
        url_block = block.select_one('a.ref_goods_n_p')
        if not url_block:
            logger.error('no url_block')
            return
        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return
        url = 'https://www.wildberries.ru' + url
        
        #-----------ЦЕНА/СКИДКА-----------
        
        cost = block.select_one('span.lower-price')
        discount='0%'
        oldcost='-'
        if not cost:
            cost = block.select_one('ins.lower-price')
            if not cost:
                logger.error(f'no cost_block in {url}')
                return
            
            oldcost = block.select_one('del')
            oldcost=oldcost.text.strip()
            
            discount = block.select_one('span.price-sale.active')
            discount=discount.text.strip()
            
        cost=cost.text.strip()

        
        #-----------ПОИСК ИМЕННОГО БЛОКА-----------
        
        name_block = block.select_one('div.dtlist-inner-brand-name')
        if not name_block:
            logger.error(f'no name_block in {url}')
            return
        
        #-----------НАИМЕНОВАНИЕ БРЭНДА-----------
        
        brand_name = name_block.select_one('strong.brand-name.c-text-sm')
        if not brand_name:
            logger.error(f'no brand_name in {url}')
            return
        brand_name=brand_name.text
        brand_name=brand_name.replace('/','').strip()
        
        #-----------НАИМЕНОВАНИЕ ВЕЩИ-----------
        
        goods_name = name_block.select_one('span.goods-name.c-text-sm')
        if not goods_name:
            logger.error(f'no goods_name in {url}')
            return
        goods_name=goods_name.text.strip()
        
        #-----------ЗАПОЛНЕНИЕ ВЫВОДА-----------
        self.result.append(ParserResult(
            brand_name=brand_name,
            goods_name=goods_name,
            cost=cost,
            oldcost=oldcost,
            discount=discount,
            url=url
        ))
        
        logger.debug('%s, %s, %s, %s', url, brand_name, goods_name, cost)
        logger.debug('-' * 90)
    
    def save_result(self):
        path = './result_WB.csv'
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
    
