import requests
import json
from random import randrange

BASE_URL = 'https://freefakeapi.io/api/comments'

CodeAbsolute = 201
TimeRespAbsolute = 5 #sec
SizeRespAbsolute = 300 #byte
new_product = {
    "content": "This is the comment content",
    "user": 1,
    "post": 5
}

#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

class TEST_IT:
    
    Etalon_JSON_MODEL={}
    Test_JSON_MODEL={}
    Header_MODEL={}
    header_eq={}
    
    def TestHeader(self, EtalonHeader, TestHeader, Key):
        Etalon=(json.loads(str(EtalonHeader).replace("'",'"'))).keys()
        Test=(json.loads(str(TestHeader).replace("'",'"'))).keys()
        if Etalon == Test:
            self.header_eq[Key]=True
            return True
        else: 
            self.header_eq[Key]=True
            return False
    
    def CheckKey(self, response, check):
        for key in response:
            # print(key, " --- ", response[key], " --- ", type(response[key]))
            if check==0:
                self.Etalon_JSON_MODEL[key]=type(response[key])
            elif check==1:
                self.Test_JSON_MODEL[key]=type(response[key])
            elif check==2:
                self.Header_MODEL[key]=type(response[key])
            
            if check != 2 and type(response[key]) == type({}):
                resp1 = response[key]
                self.CheckKey(resp1, check)
                    
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

    def EtalonJSON(self, check):
        jack = json.dumps(new_product)
        json4ik = json.loads(jack)
        
        if check==1: #проверка параметров JSON
            for key in json4ik:
                print(key, " --- ", json4ik[key], " --- ", type(json4ik[key]))    
            
        self.Etalon_JSON = requests.post(f"{BASE_URL}", json=json4ik, timeout = 5)
        print('Время загрузки:\n', self.Etalon_JSON.elapsed.total_seconds())
        self.CheckKey(self.Etalon_JSON.json(),0)
        print('\nКод:\n',self.Etalon_JSON)
        print('\nHeader-ответа:\n',self.Etalon_JSON.headers)
        print('\nЭталон ответа:\n',self.Etalon_JSON.json(),"\n")
    
    def CodeResponse(self):
        if self.Etalon_JSON.status_code == CodeAbsolute:
            print("\tТест пройден")
            return True
        else:
            print('Код:\n',self.Etalon_JSON)
    
    def TimeRespTest(self):
        if self.Etalon_JSON.elapsed.total_seconds() < TimeRespAbsolute:
            print("\tТест пройден")
        else:
            print('Время загрузки:\n', self.Etalon_JSON.elapsed.total_seconds())
    
    def SizeRespTest(self):
        if self.Etalon_JSON.text.__len__() <= SizeRespAbsolute:
            print("\tТест пройден")
        else:
            print('Размер ответа:\n', self.Etalon_JSON.text.__len__())
    
    def EquivalentsAPIschema(self):
        jack = json.dumps(new_product)
        json4ik = json.loads(jack)
        check1=0
        check2=0
        for k in json4ik.keys():
            if type(json4ik[k]) == int:
                check1+=1
                json4ik[k] = str(json4ik[k])
                Test_JSON = requests.post(f"{BASE_URL}", json=json4ik)
                self.CheckKey(Test_JSON.json(),1)
                self.CheckKey(Test_JSON.headers,2)                
                if self.TestHeader(self.Etalon_JSON.headers , Test_JSON.headers, "json-"+k)==False or self.Etalon_JSON.status_code != Test_JSON.status_code or self.Etalon_JSON_MODEL!=self.Test_JSON_MODEL:
                    print(k," - Параметр не эквивалентен в ответе")
                    check2+=1
        if check1>0 and check2 == 0:
            print("\tТест пройден")
        elif check1==0:
            print("\tТестируемые элементы не найдены")
    
    def EquvivalentsHeader(self):
        if False not in self.header_eq.values():
            print("\tТест пройден")
        else:
            print("Header-не соответствует эталону по ключу:")
            for k in self.header_eq.keys():
                if self.header_eq[k] == False:
                    print("\t",k)
    
    def HTTPs(self):
        if "https:" in BASE_URL:
            BASE_URL.replace("https:", "http:")
        elif "http:" in BASE_URL:
            BASE_URL.replace("http:", "https:")
        jack = json.dumps(new_product)
        json4ik = json.loads(jack)
        Test_JSON = requests.post(f"{BASE_URL}", json=json4ik)
        self.CheckKey(Test_JSON.json(),1)
        if self.Etalon_JSON.status_code == Test_JSON.status_code and self.Etalon_JSON_MODEL==self.Test_JSON_MODEL:
            print("\tТест пройден")
        else:
            if self.Etalon_JSON.status_code != Test_JSON.status_code:
                print("Код ответа не соответствует\n")    
            if self.Etalon_JSON_MODEL != self.Test_JSON_MODEL:
                print("Эталон не соответствует тестовой модели\n")
            print("Контент\n",new_product)
            print('Код:\n',Test_JSON)
            print('Тест:\n',Test_JSON.json(),'\n',self.Test_JSON_MODEL)              
        
    def TestFillJson(self): 
        # new_product.pop("post")
        check={}
        for k in new_product.keys():
            jack = json.dumps(new_product)
            json4ik = json.loads(jack)
            json4ik.pop(k)
            Test_JSON = requests.post(f"{BASE_URL}", json=json4ik)
            self.CheckKey(Test_JSON.json(),1)
            if self.Etalon_JSON.status_code == Test_JSON.status_code and self.Etalon_JSON_MODEL==self.Test_JSON_MODEL:
                print("Контент\n",json4ik)
                print('Код:\n',Test_JSON)
                print('Тест:\n',Test_JSON.json(),'\n',self.Test_JSON_MODEL)                
                check[k]=False
            else:
                check[k]=True
        if False not in check.values():
            print("\tТест полноты схемы пройден")
            
    def TestQualityJson(self):   
        check={}
        for k in new_product.keys():
            jack = json.dumps(new_product)
            jack=jack.replace(k,k+"111")
            json4ik = json.loads(jack)
            Test_JSON = requests.post(f"{BASE_URL}", json=json4ik)
            self.CheckKey(Test_JSON.json(),1)
            if self.Etalon_JSON.status_code == Test_JSON.status_code and self.Etalon_JSON_MODEL == self.Test_JSON_MODEL:
                print("Контент\n",json4ik)
                print('Код:\n',Test_JSON)
                print('Тест:\n',Test_JSON.json(),'\n',self.Test_JSON_MODEL)                
                check[k]=False
            else:
                check[k]=True
        if False not in check.values():
            print("\tТест качества схемы пройден")                
            
    def TestCookies(self):
        if 'Set-Cookie' in self.Etalon_JSON.headers.keys():
            check=[]
            for k in new_product.keys():
                jack = json.dumps(new_product)
                if type(new_product[k])==int:
                    for i in range(10):
                        q = randrange(100)
                        json4ik = json.loads(jack)
                        json4ik[k] = q
                        Test_JSON = requests.post(f"{BASE_URL}", json=json4ik)
                        check.append(self.Etalon_JSON.headers['Set-Cookie'])
                    # break
            mylist = list(set(check))
            if check.__len__()>mylist.__len__():
                print("\tНайдены дубликаты данных: Set-Cookie")
                print("\tУникальных параметров Set-4Cookie: ",mylist.__len__(), " из ", check.__len__())
        else:
            print("--- передача Coockie не выявлена")
    
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
    
    def run (self):
        print("########### Этап №1 - ЭТАЛОН #######################")
        self.EtalonJSON(0)
        print("########### Этап №2 - Testing ######################")
        print("########### Тест №1 - Code response ################")
        if self.CodeResponse() == True:
            print("########### Тест №2 - Time for response ############")
            self.TimeRespTest()            
            print("########### Тест №3 - Size for response ############")
            self.SizeRespTest()
            print("########### Тест №4 - Equivalents API ##############")
            self.EquivalentsAPIschema()
            print("########### Тест №5 - Equivalents header ###########")
            self.EquvivalentsHeader()
            print("########### Тест №6 - HTTP\HTTPS ###################")
            self.HTTPs()
            print("########### Тест №7 - TestFill######################")
            self.TestFillJson()
            print("########### Тест №8 - TestQuality###################")
            self.TestQualityJson()
            print("########### Тест №9 - TestCookies###################")
            self.TestCookies()

#-----------ЗАПУСК-----------
if __name__ == '__main__':

    parser = TEST_IT()
    parser.run()