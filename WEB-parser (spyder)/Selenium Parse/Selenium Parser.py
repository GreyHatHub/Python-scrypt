from selenium import webdriver
from selenium.webdriver.common.by import By

import time

try:    
    driver = webdriver.Chrome()
    keyword = "geeksforgeeks"
      
    # get geeksforgeeks.org
    driver.get("https://www.geeksforgeeks.org/")
      
    # get element 
    element = driver.find_element(By.XPATH, "//input[contains(@class, 'ant-input-lg')]")
    element.send_keys("ssss")
    print(element) 
    
    element = driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-lg')]/span")
    element.click()
    
    # print complete element
    print(element)
    
finally:
    # успеваем скопировать код за 30 секунд
    time.sleep(15)
    # закрываем браузер после всех манипуляций
    driver.quit()
    
