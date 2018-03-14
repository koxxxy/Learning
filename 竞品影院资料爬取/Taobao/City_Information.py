from lxml import etree
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import datetime
import pymysql
import re

def Connect_Mysql(SQL_TEXT):
    db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset ='utf8')
    cursor = db.cursor()
    try:
       # 执行sql语句
        cursor.execute(SQL_TEXT)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('错误回滚')
    # 关闭数据库连接
    db.close()

headers_PC = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
headers_H5 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

CityList_Url = 'https://dianying.taobao.com/cinemaList.htm'


driver = webdriver.Chrome(executable_path='E:\\PythonProject\\chromedriver.exe')
# driver = webdriver.PhantomJS()
driver.get(CityList_Url)
sleep(3)

driver.find_element_by_id('cityName').click()
sleep(1)

soup = BeautifulSoup(driver.page_source, 'lxml')
city_div = soup.find('div', class_="M-cityList scrollStyle")
city_list_a = city_div.find_all('a')

# city_list = {}
list_cityId = []
list_cityUrl = []
list_cityName = []
list_timenow = []

for city in city_list_a:
    # city_list[city.text] = city.get('href')
    list_cityId.append(city.get('data-id'))
    list_cityUrl.append('https://dianying.taobao.com' + city.get('href'))
    list_cityName.append(city.text)
    list_timenow.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
driver.close()

for i in range(0, 338):
    sql = """INSERT INTO city_taobao(CITY_ID, CITY_NAME, CITY_URL, UPDATE_TIME)
             VALUES ('%s', '%s', '%s', '%s')""" % (list_cityId[i], list_cityName[i], list_cityUrl[i], list_timenow[i])
    Connect_Mysql(sql)


