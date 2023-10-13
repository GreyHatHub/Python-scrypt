import os
import requests as req
from bs4 import BeautifulSoup

def get_file(url):
    r = requests.get(url, stream=True)
    return r


def get_name(url):
    name = url.split('/')[-1]
    
    #   каждый файл в отдельный каталог
    #folder = name.split('.')[0]

    #   в нужную папку
    folder = "NORD_OVPN"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.abspath(folder)
    return path + '/' + name
        
def save_image(name, file_object):
    with open(name, 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)

resp = req.get(url)

soup = BeautifulSoup(resp.text, 'lxml')

k=0
for tar in soup.find_all("li"):
    for tag in tar.find_all("a"):
        url = tag['href']
        if "nordvpn.com.udp" in url:
            k=k+1
            print(k, " --- ", tag['href'])
            save_image(get_name(url), get_file(url))

print("\n####################")            
print("Работа завершена")
print("####################")  