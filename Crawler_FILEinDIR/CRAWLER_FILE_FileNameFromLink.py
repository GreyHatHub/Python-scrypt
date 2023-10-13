import fake_useragent
import os
import requests as req
from bs4 import BeautifulSoup
import urllib.request

# =============================================================================
start_url = 'https://URL/uploads/documents/'
exe = '.doc'
# =============================================================================
user = fake_useragent.UserAgent().random
Header = {'User-Agent': user}
# =============================================================================

class CrawlerFile:

    # =============================Вариант №1======================================
    def get_file(self, url):
        r = req.get(url, stream=True, headers = Header)
        return r
            
    def save_file_v1(self, name, file_object):
        with open(name, 'wb') as f:
            for chunk in file_object.iter_content(8192):
                f.write(chunk)
        return file_object
    
    # =============================Вариант №2======================================
    def save_file_v2(self, urla, name):
        p = req.get(urla, headers = Header)
        out = open(name, "wb")
        out.write(p.content)
        out.close()
        return p
    
    # =============================================================================
    def get_name(self, url):
        name = url.split('/')[-1]
        
        #   каждый файл в отдельный каталог
        #folder = name.split('.')[0]
    
        #   в нужную папку
        folder = "DOWNLOAD"
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = os.path.abspath(folder)
        return path + '/' + name
    
    def run(self, url: str, file: str, k: int):
        print(" ----> " ,url)
        print(" ----> " ,file)
        k=0
        for k in range(31000, 1, -1):
            url2 = url + str(k) + file
            try:
                urllib.request.urlopen(url2)
                #---Вариант №1
                resu = self.save_file_v1(self.get_name(url2), self.get_file(url2))
                #---Вариант №2
                # resu = self.save_file_v2(url2, self.get_name(url2))
                print(k, " --- ", resu, " --- ")
            except Exception:
                print(k, " --- FALSE")
    # =============================================================================

if __name__ == '__main__':
    crawler = CrawlerFile()
    crawler.run(start_url, exe, 0)
    
    print("\n####################")            
    print("Работа завершена")
    print("####################")