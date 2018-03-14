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

# 查询数据库中城市url
db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
cursor = db.cursor()
sql = "SELECT ID, CITY_URL, CITY_NAME FROM city_taobao"
cursor.execute(sql)
results = cursor.fetchall()
Dict_CityUrltoCityName = {}
Dict_CityUrltoId = {}
List_CityUrl = []
List_CityName = []
List_ID = []
try:
    for i in results:
        List_ID.append(i[0])
        List_CityUrl.append(i[1])
        List_CityName.append(i[2])
except:
    print("Error: unable to fetch data")
else:
    Dict_CityUrltoCityName = dict(zip(List_CityUrl, List_CityName))
    Dict_CityUrltoId = dict(zip(List_CityUrl, List_ID))
    # 关闭数据库连接
    db.close()


for city in List_CityUrl[204:205]:
    CityName = Dict_CityUrltoCityName[city]
    CityId = Dict_CityUrltoId[city]
    driver = webdriver.Chrome(executable_path='E:\\PythonProject\\chromedriver.exe')
    driver.get(city)
    sleep(3)
    # 关闭广告页面
    driver.find_element_by_xpath('/html/body/div[6]/div/a[1]').click()
    sleep(1)
    # 判断是否需要点击
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/a')
        sleep(1)
    except:
        flag = False
    else:
        flag = True
    # 循环点击加载
    while flag:
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/a').click()
            sleep(1)
        except:
            flag = False
            print('页面加载出错')
        else:
            flag = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/a').is_displayed()
    # 转换Html
    page_source = driver.page_source
    cinema_tree = etree.HTML(page_source)
    cinema_lis = cinema_tree.xpath('//ul[@class="sortbar-detail J_cinemaList"]/li')
    list_cinemaUrl = []
    list_cinemaId = []
    list_cinemaName = []
    list_cinemaAdd = []
    list_cinemaTel = []
    list_cinemaCity = []
    list_timeNow = []
    # 爬取页面信息
    for lis in cinema_lis:
        cinema_url = lis.xpath('.//div[@class="middle-hd"]/h4/a/@href')[0]
        cinema_id = re.findall(r'cinemaId=\d{1,10}',cinema_url)[0].strip('cinemaId=')
        cinema_name = lis.xpath('.//div[@class="middle-hd"]/h4/a')[0].text
        cinema_add = lis.xpath('.//span[@class="limit-address"]')[0].text
        cinema_tel = cinema_tel = lis.xpath('.//div[@class="middle-p-list"]/text()')[0].strip('[]')
        list_cinemaUrl.append(cinema_url)
        list_cinemaId.append(cinema_id)
        list_cinemaName.append(cinema_name)
        list_cinemaAdd.append(cinema_add)
        list_cinemaTel.append(cinema_tel)
        list_cinemaCity.append(CityName)
        list_timeNow.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '第', CityId, '个城市', CityName, '爬取完毕，正在写入数据库')

    for a in range(0, len(list_cinemaId)):
        sql1 = """INSERT INTO cinemaname_taobao(CINEMA_ID, CINEMA_NAME, CINEMA_CITY, CINEMA_URL, UPDATE_TIEM)
             VALUES ('%s', '%s', '%s', '%s', '%s')""" % (list_cinemaId[a], list_cinemaName[a], list_cinemaCity[a], list_cinemaUrl[a], list_timeNow[a])
        # Connect_Mysql(1)
        db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql1)
        db.commit()
        db.close()
    print("%-20s写入[cinemaname_taobao]数据库成功" % '')

    for b in range(0, len(list_cinemaId)):
        sql2 = """INSERT INTO information_taobao(CINEMA_ID, TELEPHONE, ADDRESS, UPDATE_TIME)
             VALUES ('%s', '%s', '%s', '%s')""" % (list_cinemaId[b], list_cinemaAdd[b], list_cinemaTel[b], list_timeNow[b])
        db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql2)
        db.commit()
        db.close()
    print("%-20s写入[city_taobao]数据库成功" % '')

    # 关闭浏览器
    driver.close()

