from multiprocessing import Pool
import fake_useragent
import os
import requests as req
from bs4 import BeautifulSoup

# =============================================================================
start_url = 'http://URL/uploads/'
count_thread = 8
# =============================================================================


class CrawlerFile:
    
    # =============================Вариант №1======================================
    def get_file(self, url):
        Header = {'User-Agent': fake_useragent.UserAgent().random}
        r = req.get(url, stream=True, headers = Header)
        return r
            
    def save_file_v1(self, name, file_object):
        with open(name, 'wb') as f:
            for chunk in file_object.iter_content(8192):
                f.write(chunk)
        return file_object
    
    # =============================Вариант №2======================================
    def save_file_v2(self, urla, name):
        Header = {'User-Agent': fake_useragent.UserAgent().random}
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
# =============================================================================    
    def get_all_links(self, url):
        Header = {'User-Agent': fake_useragent.UserAgent().random}
        html = req.get(url, headers = Header)
        soup = BeautifulSoup(html.text, 'lxml')
        tds = soup.find('table').find_all('tr')
        links = []
        for td in tds:
            for a in td.find_all("a"):
                link = url + a['href']
                links.append(link)
        return links     
# =============================================================================
    def set_load(self, url2: str):
        file_extension = os.path.splitext(url2)
        if '?' and ';' not in url2:
            if url2[-2] not in "//":
                if file_extension[1].__len__()>1:
                    #---Вариант №1
                    resu = self.save_file_v1(self.get_name(url2), self.get_file(url2))
                    #---Вариант №2
                    # resu = self.save_file_v2(url2, self.get_name(url2))
                    print(resu, "---", url2)
                    e=1
                else:
                    alllinks = self.get_all_links(url2)
                    print("---->" ,url2, "----> всего:", alllinks.__len__())
# =============================================================================        
    def run(self, url):
        all_links = self.get_all_links(url)
        print("---->" ,url, "----> всего:", all_links.__len__())
        with Pool(count_thread) as p:
            p.map(self.set_load, all_links[5:])
# =============================================================================

if __name__ == '__main__':
    crawler = CrawlerFile()
    crawler.run(start_url)
    
    print("\n####################")            
    print("Работа завершена")
    print("####################")
