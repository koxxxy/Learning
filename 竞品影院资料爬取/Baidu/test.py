import pymysql
import requests
import datetime
from selenium import webdriver
from time import sleep
from lxml import etree

# 生成访问抬头信息
headers_PC = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
headers_H5 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

# 创立数据库连接渠道
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

city_id = []
city_name = []
dict_cityIdtoName = {}
dict_cityNametoId = {}
cityListUrl = 'http://dianying.baidu.com/common/city/citylist?hasLetter=false&isjson=false&channel=&client='
cityAdr = requests.get(cityListUrl, headers=headers_PC)
all_data = cityAdr.json()
city_data = all_data['data']['all']
for x in city_data:
    city_id.append(x['id'])
    city_name.append(x['name'])

# for z in range(0, 441):
#     sql = """INSERT INTO city_baidu(CITY_ID, CITY_NAME)
#          VALUES ('%s', '%s')""" % (city_id[z], city_name[z])
#     Connect_Mysql(sql)
print(len(city_id))