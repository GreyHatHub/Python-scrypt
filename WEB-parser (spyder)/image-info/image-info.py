from selenium import webdriver
from time import sleep
from PIL import Image
from pytesseract import image_to_string

PATH_DRIVE = "./chromedriver"

class Bot:

    def __init__(self):
        self.driver = webdriver.Chrome(PATH_DRIVE) # or Firefox() or smth else
        self.navigate()

    def take_screenshot(self):
        self.driver.save_screenshot('avito_screenshot.png')

    def tel_recon(self):
        image = Image.open('tel.gif')
        print(image_to_string(image))

    def crop(self, location, size):
        image = Image.open('avito_screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']
        image.crop((x, y, x+width, y+height)).save('tel.gif')
        self.tel_recon()

    def navigate(self):
        self.driver.get('https://www.avito.ru/velikie_luki/telefony/telefon_iphone_12_mini_128g_2093341717')
        button = self.driver.find_element_by_xpath(
            'button[@class="button item-phone-button js-item-phone-button"]')
        button.click()

        sleep(3)

        self.take_screenshot()

        image = self.driver.find_element_by_xpath(
            '//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        location = image.location
        size = image.size

        self.crop(location, size)


def main():
    b = Bot()


if __name__ == '__main__':
    main()
