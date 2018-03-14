import requests
import json
import datetime
import pymysql

Url = 'http://piaofang.maoyan.com/cinema/filter?typeId=0&date=2017-12-31&offset=0&limit='
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'piaofang.maoyan.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

Loading = True
limitNum = 9999
Num = 0

while Loading:
    try:
        MaoyanUrl = Url + str(limitNum)
        r = requests.get(MaoyanUrl, headers = headers, timeout = 30)
        r.encoding = 'UTF-8'
        jd_page = json.loads(r.text)
        Loading = jd_page['success']
        cinemaLists = jd_page['data']['list']
    except KeyError:
        Loading = True
        Num += 1
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '页面获取超时，正重新获取', str(Num).zfill(3))
    else:
        Loading = False

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '正在爬取页面信息')

List_CinemaId = []
List_CinemaName = []
List_CinemaUrl = []
List_UpdateTime = []
for list in cinemaLists:
    cinemaId = list['cinemaId']
    cinemaName = list['cinemaName']
    List_CinemaId.append(cinemaId)
    List_CinemaName.append(cinemaName)
    List_CinemaUrl.append('http://piaofang.maoyan.com/company/cinema/' + str(cinemaId) + '/opdata?dateType=3')
    List_UpdateTime.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '正在写入数据库')
db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')

for date in range(0,len(List_CinemaId)):
    sql = """INSERT INTO cinema_list_maoyanpiaofang(CINEMAID, CINEMANAME, CINMEAURL, UPDATETIME)
         VALUES ('%s', '%s', '%s', '%s')""" % (List_CinemaId[date], List_CinemaName[date], List_CinemaUrl[date], List_UpdateTime[date])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
db.close()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '数据库写入完成')
