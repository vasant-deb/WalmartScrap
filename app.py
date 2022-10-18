import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from datetime import datetime
import re
import pymysql
from datetime import datetime, timedelta
import random
from flask import Flask
from flask import jsonify
from selenium.webdriver.firefox.options import Options
import json

app = Flask(__name__)
prices_list = []
products_list = []
function1_success = False
function2_success = False
function3_success = False
function4_success = False
function5_success = False
function6_success = False
function7_success = False
function8_success = False

@app.route('/')
def hello_world():
    return 'Hello World!'

def getalldata(url,check):
     print(url)
     options = Options()
     options.headless = True
     driver = webdriver.Firefox(options=options, executable_path='geckodriver.exe')
     driver.fullscreen_window()
     driver.delete_all_cookies()
     driver.get(url)
           
     prices = WebDriverWait(driver, 100).until(
      EC.presence_of_all_elements_located((By.CLASS_NAME,'css-8frhg8'))
     )
     products = WebDriverWait(driver, 100).until(
      EC.presence_of_all_elements_located((By.CLASS_NAME,'css-1w5o70g'))
     )
     for t in range(len(products)):
        products_list.append(products[t].text)
     for p in range(len(prices)):
        prices_list.append(prices[p].text)
     print(products[0].text)
     print(len(prices_list))
     print(len(products_list))
     driver.quit()
     
     if check == True:
            #dataframe create
            print('hello')
            pr=[]
            pi=[]
            for i in range(0,len(products_list)):
                pr.append(products_list[i])
            for j in range(0,len(prices_list)):
                pi.append(prices_list[j])

            pr = np.array(pr)
            pi = np.array(pi)


            datasetx = pd.DataFrame({'price': pi, 'product': pr,'date':datetime.today().strftime('%Y-%m-%d')}, columns=['price', 'product','date'])

            datasetx.to_json(r'fruitsVegetables.json')

            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)
            datasetx.head()
            #function8
            connection = pymysql.connect(host='unity.herosite.pro',
                             user='nkbsatak_walmart',
                             password='nf#uS.OK]}9K',
                             db='nkbsatak_walmart')
            cursor = connection.cursor()
            #original data insertion
            for i in range(0,len(datasetx)):
                sql = "INSERT INTO `products` (`name`, `price`) VALUES (%s, %s)"
                price=datasetx['price'][i]

                if price.find("¢")!=-1:
                    price=re.sub(r'[^0-9.]', '', price)
                    price=int(price)/100
                    price="{:.2f}".format(price)
                    price=float(price)
                else:
                    price=float(re.sub(r'[^0-9.]', '', price))
                    price="{:.2f}".format(price)
                    price=float(price)

                cursor.execute(sql,(datasetx['product'][i],price))

            connection.commit()

     return 'success'
   
@app.route('/grocery')
def getdata():
    getalldata('https://www.walmart.ca/browse/grocery/fruits-vegetables/10019-6000194327370?icid=grocery_wm_OGL1_LMagCategory_Tile_Fruits_Veg&p=1','false')  
    function1_success = True
    if function1_success:
            getalldata('https://www.walmart.ca/browse/grocery/fruits-vegetables/10019-6000194327370?icid=grocery_wm_OGL1_LMagCategory_Tile_Fruits_Veg&p=2','false')
            function2_success = True
            
    if function2_success:

            getalldata('https://www.walmart.ca/browse/grocery/fruits-vegetables/10019-6000194327370?icid=grocery_wm_OGL1_LMagCategory_Tile_Fruits_Veg&p=3','false')
            function3_success = True
            
    if function3_success:
            #page4
            getalldata('https://www.walmart.ca/browse/grocery/fruits-vegetables/10019-6000194327370?icid=grocery_wm_OGL1_LMagCategory_Tile_Fruits_Veg&p=4','false')
            function4_success = True

    if function4_success:
            #page5
            getalldata('https://www.walmart.ca/browse/grocery/fruits-vegetables/10019-6000194327370?icid=grocery_wm_OGL1_LMagCategory_Tile_Fruits_Veg&p=5','false')
            function5_success = True

    if function5_success:
            #page6
            function6_success = True
            mychecknew=getalldata('https://www.walmart.ca/browse/grocery/fruits-vegetables/10019-6000194327370?icid=grocery_wm_OGL1_LMagCategory_Tile_Fruits_Veg&p=6',function6_success)
            
    return mychecknew
    

if __name__ == '__main__':
    app.run()

