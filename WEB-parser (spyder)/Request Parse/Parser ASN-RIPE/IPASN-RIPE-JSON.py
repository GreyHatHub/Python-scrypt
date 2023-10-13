import logging
import collections

import requests
import json
import csv

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('RIPE')


ParserResult = collections.namedtuple(
    'ParseResult',
    (
         'brand_name',
         'goods_name',
         'ippref',
         'url'
    )
)

HEADERS = ( 'Name', 'Info', 'IP-Range', 'Link')

Target = "ZB"


class Parser:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0', 
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.result = []
    
    #-----------Load first page-----------   
    def load_page(self, text: str, nums: int, page: int = None):
        if nums == 0: #List ASN
            url = 'https://stat.ripe.net/data/country-resource-list/data.json?resource='+text
            res = self.session.get(url = url)
            res.raise_for_status()
            return res.text
        if nums == 1: #Info ASN
            url = 'https://stat.ripe.net/data/as-overview/data.json?resource='+text
            res = self.session.get(url = url)
            # res.raise_for_status()
            return res.text
        if nums == 2: #List IP
            url = 'https://stat.ripe.net/data/as-routing-consistency/data.json?resource='+text
            res = self.session.get(url = url)
            # res.raise_for_status()
            return res.text
        if nums == 3: #Info IP
            url = 'https://stat.ripe.net/data/prefix-routing-consistency/data.json?resource='+text
            res = self.session.get(url = url)
            # res.raise_for_status()
            return res.text                      
   
    #-----------Parsing page-----------   
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
            block='AS'+block
            
            print('#'*20+f' {i} from {gjson.__len__()} '+'#'*20)
            # logger.debug('%s from %s', i, gjson.__len__())
            
            ### PARSE ASN ###
            self.parse_block(block=block)
            ### SAVE RESULT ###
            self.html_table()
            self.save_result()
            print('-'*90)
        
    def parse_block (self, block):
        
        brand_name = block
        #-----------Name ASN-----------
        
        goods_name = json.loads(self.load_page(text=block, nums=1))
        goods_name = goods_name['data']
        for key in goods_name:
            if key == 'holder':
                goods_name = goods_name[key]
                break
        
        #-----------Range IP-----------
        
        ipprefs = []
        ipp = ''
        bloks = json.loads(self.load_page(text=block, nums=2))
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
                            if k['asn_name'] == brand_name:
                                s = s + ' ' + k['asn_name']
                                globipprefs.append(s)
                    else:
                        for k in bloks:
                            globipprefs.append(k['prefix'] + ' ' + k['asn_name'])
        for k in globipprefs:
            if k not in ipp:
                ipp=ipp + k+', '
        
		#-----------Load out-----------
        self.result.append(ParserResult(
		    brand_name=brand_name,  #ASN
		    goods_name=goods_name,  #Name
		    ippref=ipp,         #IP-Range
            url=''             #not use
		))
		
        # logger.debug('%s, %s, %s, %s', brand_name, goods_name, ipprefs, url)
        logger.debug('-' * 90)
    
    #-----------Save Table CSV-----------
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
        # href="<a href=\"{0}\">"
        subitems = [tr.format(''.join([td.format(item[i]) for i in range(len(item)-1)])) for item in self.result]
        
        display = open("result_provider.html", 'w')
        display.write(html.format("".join(subitems),'{','}'))
    
    #-----------Call function-----------
    def run (self):
        text = self.load_page(text=Target, nums=0)
        # logger.info(' Page load')
        self.pars_page(text=text)
        # logger.info(f' get {len(self.result)} provider')
        
        # self.graph_pdf()
        self.save_result()
        self.html_table()

#-----------Start-----------        
if __name__ == '__main__':
    parser = Parser()
    parser.run()
