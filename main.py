
from selenium import webdriver

from time import *

from re import *

from PIL import Image

from pytesseract import pytesseract

import random

import os

import schedule

todayCodes = []

PROXY = '37.32.14.207:17280'

chDrURL = '/Users/MeT/Code/Telegram Bot/Self Beheshti/chromedriver'

class Code:

    def __init__(self, num,  seller, buyer, checked, used):

        self.num = num

        self.seller = seller

        self.buyer = buyer

        self.used = used

        self.checked = checked
        
    def check(self):
        
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        
        driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
        
        driver.get('https://dining.sbu.ac.ir/index.rose')
        
        driver.find_element('id' , 'username').send_keys(self.seller.studentId)
        
        driver.find_element('id' , 'password').send_keys(self.seller.idNumber)
        
        driver.find_element('id' , 'login_btn_submit').click()
        
        sleep(1)
        
        if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
            
            driver.close()
            
            return False
        
        driver.get('https://dining.sbu.ac.ir/student/forgetCard/getCode/list.rose')
        
        sleep(1)
        
        reserves = driver.find_elements('xpath' , '//*[@id="reserve"]/tbody/tr')
        
        for i in range(1,len(reserves)+1):
            
            if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[7]').text == 'غذای نوع 3/5(نیم پرس)' :
                
                if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[12]/input').is_selected() == False:
                    
                    driver.find_element('xpath' , f'//*[@id="print-{i}"]').click()
                    
                    sleep(1)
                    
                    codeText = driver.find_element('xpath' , '//*[@id="printResult"]/tr[1]/td').text
                    
                    driver.close()
                    
                    code = int(findall('[0-9]+' , codeText)[0])
                    
                    self.num = code
        
                    self.checked = True
                    
                    return True
                    
        driver.close()
        
        return False
        
    def codeIndex():
    
        for idx , code in enumerate(todayCodes):
        
            if code.used == False:
              
                return idx

        return -1
        
class Seller:

    def __init__(self, code, studentId, idNumber, payedTo , chatId):

        self.code = code

        self.studentId = studentId

        self.idNumber = idNumber

        self.payedTo = payedTo
        
        self.chatId = chatId
 
    def check(self):
        
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        
        driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
        
        driver.get('https://dining.sbu.ac.ir/index.rose')
        
        driver.find_element('id' , 'username').send_keys(self.studentId)
        
        driver.find_element('id' , 'password').send_keys(self.idNumber)
        
        driver.find_element('id' , 'login_btn_submit').click()
        
        sleep(1)
        
        if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
            
            driver.close()
            
            return False
        
        driver.get('https://dining.sbu.ac.ir/student/forgetCard/getCode/list.rose')
        
        sleep(1)
        
        reserves = driver.find_elements('xpath' , '//*[@id="reserve"]/tbody/tr')
        
        for i in range(1,len(reserves)+1):
            
            if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[7]').text == 'غذای نوع 3/5(نیم پرس)' :
                
                if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[12]/input').is_selected() == False:
                    
                    driver.find_element('xpath' , f'//*[@id="print-{i}"]').click()
                    
                    sleep(1)
                    
                    codeText = driver.find_element('xpath' , '//*[@id="printResult"]/tr[1]/td').text
                    
                    driver.close()
                    
                    code = int(findall('[0-9]+' , codeText)[0])
                    
                    for c in todayCodes:
                        
                        if c.num == code:
                            
                            return False
                            
                    newCode = Code(num=code, seller=self, buyer=None, checked=False, used=False)
                    
                    self.code = newCode
                    
                    todayCodes.append(newCode)
                    
                    addCodeToFile(newCode)
                    
                    return True
                
        driver.close()
                    
        return False
        
    def payment(self):
        
        if self.payedTo == False:
        
            chrome_options = webdriver.ChromeOptions()
        
            chrome_options.add_argument(f'--proxy-server={PROXY}')
            
            driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
        
            driver.get('https://dining.sbu.ac.ir/index.rose')
        
            driver.find_element('id' , 'username').send_keys(400243043)
        
            driver.find_element('id' , 'password').send_keys(4610913976)
        
            driver.find_element('id' , 'login_btn_submit').click()
        
            sleep(1)
        
            if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
                
                driver.close()
            
                return False
        
            driver.get('https://dining.sbu.ac.ir/nurture/user/credit/inputTransferCreditInfo.rose')
        
            sleep(1)
        
            driver.find_element('id' , 'studentNumberInput').send_keys(self.studentId)
        
            driver.find_element('id' , 'transferAmount').send_keys(60000)
        
            c = driver.find_element('id' , 'captcha_img')
        
            imgName = random.randrange(1,1001)
        
            imgName = str(imgName)
        
            c.screenshot(f'{imgName}.png')
        
            sleep(1)
        
            img = Image.open(f'{imgName}.png')
        
            pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.3.0_1/bin/tesseract'
        
            captcha = pytesseract.image_to_string(img)
        
            driver.find_element('id' , 'captcha_input').send_keys(captcha)
        
            sleep(2)
        
            driver.find_element('xpath' , '/html/body/div[2]/div[4]/div[1]/div/div/div[2]/form/table/tbody/tr/td[1]/input').click()
        
            sleep(1)

            driver.close()
            
            os.remove(f'{imgName}.png')
        
            self.payedTo = True
        
            return True
        
        else:
        
            return True
        
class Buyer:

    def __init__(self, code , studentId , idNumber , isPayed):

        self.code = code

        self.isPayed = isPayed
        
        self.studentId = studentId
        
        self.idNumber = idNumber
                
    def payment(self):

        if self.isPayed == False:
        
            chrome_options = webdriver.ChromeOptions()
        
            chrome_options.add_argument(f'--proxy-server={PROXY}')

            driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
        
            driver.get('https://dining.sbu.ac.ir/index.rose')
        
            driver.find_element('id' , 'username').send_keys(self.studentId)
        
            driver.find_element('id' , 'password').send_keys(self.idNumber)
        
            driver.find_element('id' , 'login_btn_submit').click()
        
            sleep(1)
        
            if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
                
                driver.close()
            
                return False
        
            driver.get('https://dining.sbu.ac.ir/nurture/user/credit/inputTransferCreditInfo.rose')
        
            sleep(1)
        
            priceText = driver.find_element('xpath' , '/html/body/div[2]/div[4]/div[1]/div/div/div[1]/div/div').text
        
            priceText = priceText.partition('\n')[0]
        
            price = findall('[0-9]+', priceText)[0]
        
            price = int(price)
        
            if price < 80000 :
                
                driver.close()
            
                return False
        
            driver.find_element('id' , 'studentNumberInput').send_keys(400243043)
        
            driver.find_element('id' , 'transferAmount').send_keys(80000)
        
            c = driver.find_element('id' , 'captcha_img')
        
            imgName = random.randrange(1,1001)
        
            imgName = str(imgName)
        
            c.screenshot(f'{imgName}.png')
        
            sleep(1)
        
            img = Image.open(f'{imgName}.png')
        
            pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.3.0_1/bin/tesseract'
        
            captcha = pytesseract.image_to_string(img)
        
            driver.find_element('id' , 'captcha_input').send_keys(captcha)
        
            sleep(2)
        
            driver.find_element('xpath' , '/html/body/div[2]/div[4]/div[1]/div/div/div[2]/form/table/tbody/tr/td[1]/input').click()
        
            sleep(1)
            
            driver.close()
            
            os.remove(f'{imgName}.png')
        
            self.isPayed = True
        
            return True
        
        else:
        
            return True
    
    def giveCode(self):
        
        if Code.codeIndex() > -1 :
            
            index = Code.codeIndex()
            
            codeCheck = Code.check(todayCodes[index])
            
            if codeCheck:
                
                buyerPay = Buyer.payment(self)
                
                if buyerPay:
                    
                    self.code = todayCodes[index]
                    
                    todayCodes[index].used = True
                    
                    addBuyerToFile(todayCodes[index])
                    
                    return True
            else:
                
                removeCodeFromFile(todayCodes[index])
                
                del todayCodes[index]
                
                Buyer.giveCode(self)
                
        return False
    
def addCodeToFile(code):
    
    with open('Codes.txt' , 'a') as f:
        
        f.write(f'{code.num}\nSeller {code.seller.studentId} {code.seller.idNumber} {code.seller.payedTo} {code.seller.chatId}\nBuyer\n')
        
def removeCodeFromFile(code):
    
    lines = []
    
    with open('Codes.txt' , 'r') as r:
        
        lines = r.readlines()
        
    with open('temp.txt' , 'w') as w:
        
        idx = 0
        
        while idx < len(lines):
            
            if lines[idx] == f'{code.num}\n':
                
                idx += 4
                
            else:
                
                w.write(lines[idx])
                
                idx += 1
    
    os.remove('Codes.txt')
    
    os.rename('temp.txt', 'Codes.txt') 
    
def addBuyerToFile(code):
    
    lines = []
    
    with open('Codes.txt' , 'r') as r:
        
        lines = r.readlines()
        
    with open('temp.txt' , 'w') as w:
        
        idx = 0
        
        bIdx = -1
        
        while idx < len(lines):
            
            if lines[idx] == f'{code.num}\n':
                
                bIdx = idx + 2
            
            if idx == bIdx:
                
                w.write(f'Buyer {code.buyer.studentId} {code.buyer.idNumber}\n')
                
            else:
                
                w.write(lines[idx])
                
            idx += 1
            
    os.remove('Codes.txt')
    
    os.rename('temp.txt', 'Codes.txt')
    
def sellerPayToFile(code):
    
    lines = []
    
    with open('Codes.txt' , 'r') as r:
        
        lines = r.readline()
        
    with open('temp.txt' , 'w') as w:
        
        idx = 0
        
        sIdx = -1
        
        while idx < len(lines):
            
            if lines[idx] == f'{code.num}\n':
                
                sIdx = idx + 1
                
            if idx == sIdx:
                
                w.write(f'Seller {code.seller.studentId} {code.seller.idNumber} {code.seller.payedTo} {code.seller.chatId}')
                
            else:
                
                w.write(lines[idx])
                
            idx += 1
            
    os.remove('Codes.txt')
    
    os.rename('temp.txt', 'Codes.txt')
    
def textToList():
    
    lines = []
    
    with open('Codes.txt' , 'r') as r:
        
        lines = r.readlines()
    
    for idx in range(len(lines)):
        
        lines[idx] = lines[idx].replace('\n', '')
    
    for idx in range(len(lines)):
        
        if lines[idx].isnumeric():
            
            code = int(lines[idx])
            
            seller = lines[idx+1].split()
            
            buyer = lines[idx+2].split()
            
            nSeller = Seller(code=None, studentId=int(seller[1]), idNumber=int(seller[2]), payedTo=bool(seller[3]), chatId=seller[4])
            
            if len(buyer) > 1:
            
                nBuyer = Buyer(code=None, studentId=int(buyer[1]), idNumber=int(buyer[2]), isPayed=True)
            
                nCode = Code(num=code, seller=nSeller, buyer=nBuyer, checked=True, used=True)
                
                nSeller.code = nCode
                
                nBuyer.code = nCode
                
                todayCodes.append(nCode)
                
            else:
                
                nCode = Code(num=code, seller=nSeller, buyer=None, checked=False, used=False)
                
                nSeller.code = nCode
                
                todayCodes.append(nCode)
                
def clearList():
    
    todayCodes.clear()
    
    open('Codes.txt', 'w').close()
