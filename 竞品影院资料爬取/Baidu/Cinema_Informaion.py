import pymysql
import requests
import re
from time import sleep
import datetime


headers_PC = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'dianying.nuomi.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

# 查询数据库中城市url
db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
cursor = db.cursor()
sql = "SELECT * FROM cinema_list_baidu"
cursor.execute(sql)
results = cursor.fetchall()
List_Id= []
List_CinemaId = []
List_CinemaName = []
List_CinemaCtiy = []
List_CinemaUrl = []
Dict_UrltoCinemaId = {}
Dict_UrltoId = {}
print('正在读取数据库中的影院列表')
try:
    for i in results:
        List_Id.append(i[0])
        List_CinemaId.append(i[1])
        List_CinemaName.append(i[2])
        List_CinemaCtiy.append(i[3])
        List_CinemaUrl.append(i[4])
except:
    print("Error: unable to fetch data")
else:
    Dict_UrltoCinemaId = dict(zip(List_CinemaUrl, List_CinemaId))
    Dict_UrltoId = dict(zip(List_CinemaUrl, List_Id))
    # print(List_CinemaUrl)
    # 关闭数据库连接
    db.close()
    print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  ' 读取影院列表成功')
# print(List_CinemaUrl[173])

for url in List_CinemaUrl[6554:6619]:
    r = requests.get(url, headers = headers)
    r.encoding = 'UTF-8'
    page = r.text
    # print(page)
    Id = Dict_UrltoId[url]
    print('正在爬取第', str(Id).zfill(3), '个影院')
    CinemaId = Dict_UrltoCinemaId[url]
    CinemaName = re.findall(r'title font-color.{2,50}<em class', page)[0].strip(r'title font-color\">').strip('<em class')
    CinemaInformation = re.findall(r'addr font-grey.{2,200}</p>\\n ', page)[0].strip(r'addr font-grey\">')
    # print(CinemaInformation)
    try:
        CinemaAdd = re.findall(r'.{1,150}<em class=', CinemaInformation)[0].strip('<em class=')
        CinmemaTel = re.findall(r'</em>.{1,150}</p', CinemaInformation)[0].strip('</p').strip('em>')
    except IndexError:
        CinemaAdd = re.findall(r'.{1,150}</p', CinemaInformation)[0].strip('</p')
        CinmemaTel = ''
    TimeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  ' 影院' + CinemaName + '爬取成功，正在写入数据库')
    sql2 = """INSERT INTO cinema_information_baidu(CINEMA_ID, TELEPHONE, ADDRESS, UPDATE_TIME)
         VALUES ('%s', '%s', '%s', '%s')""" % (CinemaId, CinmemaTel, CinemaAdd, TimeNow)
    db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql2)
    db.commit()
    db.close()
    print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  ' 数据库写入成功')