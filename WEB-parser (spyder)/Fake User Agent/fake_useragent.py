import requests
import fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
Header = {'User-Agent': user}

link = "https://browser-info.ru"
responce = requests.get(link, headers = Header).text
soup = BeautifulSoup(responce, 'lxml')
block = soup.find('div', id = "tool_padding")

### check JS
check_js = block.find('div', id = 'javascript_check')
status_js = check_js.find_all('span')[1].text
result_js = f'javascript: {status_js}'
print(result_js)

### check Flash
check_flash = block.find('div', id = 'flash_version')
status_flash = check_flash.find_all('span')[1].text
result_flash = f'flash: {status_flash}'
print(result_flash)

### check User-Agent
check_UA = block.find('div', id = 'user_agent').text
print(check_UA)
