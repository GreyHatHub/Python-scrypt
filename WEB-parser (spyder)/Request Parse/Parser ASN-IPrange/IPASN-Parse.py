import logging
import collections
import json
import requests
from bs4 import BeautifulSoup
import csv

import  graphviz

dot  =  graphviz.Digraph(comment='The Round Table')
dot.attr(rankdir='LR', size='8,5')

logging.basicConfig(level = logging.WARNING)
logger = logging.getLogger('RIPE+IPIP')

ParserResult = collections.namedtuple(
    'ParseResult',
    (
         'brand_name',
         'goods_name',
         'ippref',
         'url'
    )
)


HEADERS = ( 'Name', 'Info', 'IP-range', 'Link')

class Parser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0', 
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.result = []
    
    #-----------Load_first_page-----------   
    def load_page(self, text: str, nums: int, page: int = None):
        if nums == 1: #List IP
            url = 'https://stat.ripe.net/data/country-resource-list/data.json?resource='+text
            res = self.session.get(url = url)
            # res.raise_for_status()
            return res.text
        if nums == 2: #List IP
            url = 'https://stat.ripe.net/data/as-routing-consistency/data.json?resource=AS'+text
            res = self.session.get(url = url)
            # res.raise_for_status()
            return res.text
        if nums == 3: #Info об IP
            url = 'https://stat.ripe.net/data/prefix-routing-consistency/data.json?resource='+text
            res = self.session.get(url = url)
            # res.raise_for_status()
            return res.text   
    
    #-----------Load_second_page-----------   
    def load_page_second(self, text=str, page: int = None):
        # text = '8633'
        url = 'https://whois.ipip.net/AS'+text
        res = self.session.get(url = url)
        soup = BeautifulSoup(res.text, 'lxml')
        Sr=''
        asname=''
        if soup:    
            #  
            container = soup.find_all('div', class_='col-sm-3')
            for block in container:
                if 'AS Name' in block.text:
                    asname = block.find('h5').text

            if not asname:
                whois = soup.find('pre')
                s = whois.text.split(sep='\n')
                for exp in s:
                    if 'as-name:' in exp and 'UNSPECIFIED' not in exp:
                        asname = exp.split()[1]
                        break
                    elif not asname and 'org-name:' in exp:
                        asname = exp.split(sep=':')[1]

            # 
            container = soup.find('table', class_='table') #seach

            if not container:
                ipprefs = []
                ipp = ''
                bloks = json.loads(self.load_page(text=text, nums=2))
                bloks = bloks['data']
                for key in bloks:
                    if key == 'prefixes':
                        bloks = bloks[key]
                        for s in bloks:
                            ipprefs.append(s['prefix'])
                globipprefs=[]
                print (ipprefs)
                for i,s in enumerate(ipprefs):
                    bloks = json.loads(self.load_page(text=s, nums=3))        
                    bloks = bloks['data']
                    for key in bloks:
                        if key == 'routes':
                            bloks = bloks[key]
                            if bloks.__len__()==1:
                                for k in bloks:
                                    s = s + ' ' + k['asn_name']
                                    globipprefs.append(s)
                            else:
                                for k in bloks:
                                    if str(k['origin']) == text:
                                        globipprefs.append(k['prefix'] + ' ' + k['asn_name'])

                for k in globipprefs:
                    if k not in ipp:
                        ipp=ipp + k+', '
                Sr=ipp
            else:
                if 'CIDR' in container.find('th'):
                    bloks = container.find_all('a')
                    for block in bloks:
                        di=block.text
                        na=block.get('title')
                        name=na
                        Sr=Sr + di+' '+name+', '
                else:
                    ipprefs = []
                    ipp = ''
                    bloks = json.loads(self.load_page(text=text, nums=2))
                    bloks = bloks['data']
                    for key in bloks:
                        if key == 'prefixes':
                            bloks = bloks[key]
                            for s in bloks:
                                ipprefs.append(s['prefix'])
                    globipprefs=[]
                    print (ipprefs)
                    for i,s in enumerate(ipprefs):
                        bloks = json.loads(self.load_page(text=s, nums=3))        
                        bloks = bloks['data']
                        for key in bloks:
                            if key == 'routes':
                                bloks = bloks[key]
                                if bloks.__len__()==1:
                                    for k in bloks:
                                        s = s + ' ' + k['asn_name']
                                        globipprefs.append(s)
                                else:
                                    for k in bloks:
                                        if str(k['origin']) == text:
                                            globipprefs.append(k['prefix'] + ' ' + k['asn_name'])
    
                    for k in globipprefs:
                        if k not in ipp:
                            ipp=ipp + k+', '
                    Sr=ipp                    
                        
        else:
            Sr='break'
        return Sr,asname
    
    #-----------Parsing data-----------   
    def pars_page (self, text: str):
        gjson = json.loads(text)
        #tasn = gjson['data']
        for key in gjson:
            if key == 'data':
                gjson = gjson[key]
                for key in gjson:
                    if key == 'resources':
                        gjson = gjson[key]
                        for key in gjson:
                            if key == 'asn':
                                gjson = gjson[key]
        for i,block in enumerate(gjson):
            i=i+1
            
            print('#'*20+f' {i} from {gjson.__len__()} '+'#'*20)
            self.parse_block(block=block)

            # self.graph_pdf()
            self.html_table()
            self.save_result()
        
    def parse_block (self, block):
        
        #-----------Name ASN-----------
        
        brand_name = "AS"+block
       
        #-----------Range IP-----------
        # goods_name - Name Company
        # ipprefs - range
        ipprefs, goods_name  = self.load_page_second(text=block)
        # ipprefs = dopparse[0]
        # whois = dopparse[1]
        
		#-----------Load out-----------
        self.result.append(ParserResult(
		    brand_name=brand_name,  #name
		    goods_name=goods_name,  #info
		    ippref=ipprefs,         #IP-range
		    url=''                 #link
		))
		
        #logger.debug('%s, %s, %s, %s', brand_name, goods_name, ipprefs, url)
        logger.debug('-' * 90)
    
    #-----------
    def graph_pdf(self):
        for item in self.result:
            z=item[3].split(',')
            for s in z:
                if s.__len__() >3:
                    dot.edge(s, item[0])
        #dot.view()
        dot.render('round-table.gv', view=True)
    
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
            <h1>IP ASN</h1>
            <table border="3" width="100%" cellpadding="4">
                {0}
            </table>
        </body>
        </HTML>"""
        tr = "<tr>{0}</tr>"
        td = "<td>{0}</td>"
        href="<a href=\"{0}\">"
        # subitems = [tr.format(''.join([td.format(href.format(item[-1]) + item[i]) for i in range(len(item)-1)])) for item in self.result]
        subitems = [tr.format(''.join([td.format(item[i]) for i in range(len(item)-1)])) for item in self.result]
        
        display = open("result_provider.html", 'w')
        display.write(html.format("".join(subitems),'{','}'))
    
    #-----------Call function-----------
    def run (self):
        country = input("[Enter country code, example 'ZB']: ")

        text = self.load_page(text = country, nums = 1)
        logger.info(f' Страница загружена')
        
        self.pars_page(text=text)
        logger.info(f' get {len(self.result)} provider')
        
        # self.save_result()
        # self.html_table()

#-----------Start-----------        
if __name__ == '__main__':
    parser = Parser()
    parser.run()