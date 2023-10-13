import logging
import collections
import datetime

import requests
import json
import csv

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('RIPE')

# 17:01:000032:12

ParserResult = collections.namedtuple(
    'ParseResult',
    (
         'Kadastr',
         'Adress',
         'Status',
         'Ploshad',
         'Cost',
         'Data',
         'xz'
    )
)

HEADERS = ( 'Кадастро', 'Адрес', 'Стутус', 'Площадь','Стоимость','ДатаВнесения','xz')


class Parser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'pkk.rosreestr.ru',
            'Referer':	'https://pkk.rosreestr.ru/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        self.result = []
    
    #-----------Load Page-----------   
    def load_page(self, nums: int, page: int = None):
        url = 'https://pkk.rosreestr.ru/api/features/1/17%3A1%3A6032%3A'+str(nums)
        for a in range(10):
            try:
                res = self.session.get(url = url, verify=False,timeout=10)
                return res.text
            except:
                print("!!!!!!!!", url)
        
        
                    
   
    #-----------Parsing-----------   
    def pars_page (self, text: str):
        gjson = json.loads(text)
        gjson = gjson["feature"]
        if gjson != None:        
             gaddress=''
             gcn=''
             garea_value=''
             gcad_cost=''
             gdate_cost=''
             for key in gjson:
                 if key == 'attrs':
                     gjson = gjson[key]
                     for key in gjson:
                         if key == 'address':
                             gaddress = gjson[key]
                             # print(gaddress)
                         if key == 'cn':
                             gcn = gjson[key]
                             # print(gcn)
                         if key == 'util_by_doc':
                             gutil_by_doc = gjson[key] 
                             # print(gutil_by_doc) 
                         if key == 'area_value':
                             garea_value = gjson[key]  
                             # print(garea_value)
                         if key == 'cad_cost':
                             gcad_cost = gjson[key]  
                             # print(gcad_cost)
                         if key == 'cc_date_entering':
                             gdate_cost = gjson[key]
                             # print(gdate_cost)
                           
             self.result.append(ParserResult(
                 Kadastr = gcn,
                 Adress = gaddress,
                 Status = gutil_by_doc,
                 Ploshad = str(garea_value) + " м2",
                 Cost = str(gcad_cost) + " руб.",
                 Data = gdate_cost,
                 xz = ''
          	 ))                
    
    #-----------Save table CSV-----------
    def save_result(self):
        path = './result_provider.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL )
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)
                
    #-----------Save table HTML-----------           
    def html_table(self):
        html = """<HTML>
        <style>
            table {1} 
                font-size: 10pt;
            {2}
        </style>
        <body>
            <h1>ТСН СТ "Милосердие"</h1>
            <table border="3" width="100%" cellpadding="4">
                {0}
            </table>
        </body>
        </HTML>"""
        tr = "<tr>{0}</tr>"
        td = "<td>{0}</td>"
        # href="<a href=\"{0}\">"
        # subitems = [tr.format(''.join([td.format(href.format(item[-1]) + item[i]) for i in range(len(item)-1)])) for item in self.result]
        subitems = [tr.format(''.join([td.format(item[i]) for i in range(len(item)-1)])) for item in self.result]
        
        display = open("result_provider.html", 'w')
        display.write(html.format("".join(subitems),'{','}'))
    
    #-----------Call function-----------
    def run (self):
        number=1
        while number < 1000: 
            text = self.load_page(nums=number)
            self.pars_page(text=text)
            self.save_result()
            self.html_table()
            number=number+1

#-----------ЗАПУСК-----------        
if __name__ == '__main__':
    parser = Parser()
    parser.run()
