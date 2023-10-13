#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import collections

import requests
from bs4 import BeautifulSoup
import csv
import  graphviz

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('GRAPH')

dot  =  graphviz.Digraph( comment='The Round Table') #engine='twopi'
dot.attr(rankdir='LR', size='8,5', ranksep='0' )

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
            'Accept-Language': 'ru',
        }
        self.result = []

    #-----------        
    def load_page_second(self, ASNnumber: str , P: str, page: int = None):
        url = 'https://whois.ipip.net/'+ASNnumber
        res = self.session.get(url = url)
        soup = BeautifulSoup(res.text, 'lxml')
        Sr=''
        whoises = ''
        nameASN = ''
        if soup:    
            whois = soup.find('pre')
            s = whois.text.split(sep='\n')
            for exp in s:
                if 'import' in exp and 'mp-import' not in exp and 'important' not in exp:
                    exp = exp.split()
                    whoises = whoises + exp[2] + ','
                if 'as-name:' in exp:
                    nameASN = exp.split()[1]
                elif not nameASN and 'org:' in exp:
                    nameASN = exp.split()[1]
                
            nameASN=ASNnumber+' '+nameASN
            if "a" in P:
                dot.node(ASNnumber, nameASN, color='crimson')
            elif "1" in P:
                dot.node(ASNnumber, nameASN, color='dodgerblue')
            elif "2" in P:
                dot.node(ASNnumber, nameASN, color='green')                
                
            whoises=whoises.split(',')
            if whoises.__len__()<50:
                for i,item in enumerate(whoises, start=0):
                    whoises[i]=item.upper()
                    if item.__len__() >3:
                        dot.edge(item, ASNnumber)
        else:
            Sr='break'
        return whoises
    
    #-----------Call function-----------
    def run (self):
        ASNnumber = input("\n[Enter number ASN, ex: AS777]: ")
        print('\n')
        if not ASNnumber:
            print('ASN not enter...')
        else:
            ipprefs = self.load_page_second(ASNnumber=ASNnumber, P="a")
            i=0
            while i < 2: # deep
                i=i + 1
                ten=[]
                for who in ipprefs:
                    if who != "":
                        a = self.load_page_second(who,str(i))
                        ten = ten + a
                ipprefs = ten
            dot.render('round-table.gv', view=True)
                
#-----------Start-----------        
if __name__ == '__main__':
    parser = Parser()
    parser.run()
