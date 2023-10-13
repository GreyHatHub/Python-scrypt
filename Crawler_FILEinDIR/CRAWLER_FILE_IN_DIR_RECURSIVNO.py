import fake_useragent
import os
import requests as req
from bs4 import BeautifulSoup

# =============================================================================
start_url = 'http://URL/uploads/'
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
    
    def run(self, url, k: int):
        print(" ----> " ,url)
        resp = req.get(url, headers = Header)
        soup = BeautifulSoup(resp.text, 'lxml')
    # =============================================================================
        for tar in soup.find_all("tr"):
            for tag in tar.find_all("a"):
                if tag['href'].__len__() > 2:
                    if '/' not in tag['href']:
                        url2 = url + tag['href']
                        k=k+1
                        #---Вариант №1
                        resu = self.save_file_v1(self.get_name(url2), self.get_file(url2))
                        #---Вариант №2
                        resu = self.save_file_v2(url2, self.get_name(url2))
                        print(k, " --- ", resu, " --- ", tag['href'])
                    else:
                        url2 = url + tag['href']
                        self.run(url2, k)
    # =============================================================================

if __name__ == '__main__':
    crawler = CrawlerFile()
    crawler.run(start_url, 0)
    
    print("\n####################")            
    print("Работа завершена")
    print("####################")