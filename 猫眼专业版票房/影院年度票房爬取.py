import pymysql
from lxml import etree
import datetime
from time import sleep
from selenium import webdriver


Url = 'http://piaofang.maoyan.com/cinema/filter?typeId=0&date=2017-12-31&offset=0&limit='
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'piaofang.maoyan.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

# 获取之前爬取的进度
def get_last_NumId():
    db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
    cursor = db.cursor()
    sql = "select ID from cinema_list_maoyanpiaofang WHERE CINEMAID = (select CINEMA_ID from cinema_piaofang_maoyanpiaofang order by ID DESC limit 0,1 )"
    cursor.execute(sql)
    results = cursor.fetchall()
    return str(results[0]).strip('(),')

# 查询数据库中影院
db = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
cursor = db.cursor()
sql = "SELECT * FROM cinema_list_maoyanpiaofang"
cursor.execute(sql)
results = cursor.fetchall()
List_Id= []
List_CinemaId = []
List_CinemaName = []
Dict_IDtoName = {}
print('正在读取数据库，准备爬取数据...')
for list in results:
    List_Id.append(list[0])
    List_CinemaId.append(list[1])
    List_CinemaName.append(list[2])
Dict_CinemaIDtoName = dict(zip(List_CinemaId, List_CinemaName))
db.close()

min = int(get_last_NumId())
max = len(List_Id)

# db2 = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
# cursor2 = db2.cursor()
# print('开始爬取影院票房数据，已完成', str(min), '家，剩余', str(max - min), '家')
# # for num in range(0,1):
# # for num in range(0,len(List_Id)):
# for num in range(min, max):
#     CienmaID = List_CinemaId[num]
#     CinemaName = List_CinemaName[num]
#     print('总', str(max), '家影院，正在爬取第', str(num + 1), '家影院', CinemaName)
#     riqi = []
#     piaofang = []
#     changjunrenci = []
#     danzuopiaofang = []
#     CinemaUrl = 'http://piaofang.maoyan.com/company/cinema/' + str(CienmaID)
#     driver = webdriver.Chrome(executable_path='E:\\PythonProject\\chromedriver.exe')
#     driver.get(CinemaUrl)
#     sleep(3)
#     driver.find_element_by_xpath('//*[@id="op-view"]/div[1]/ul/li[4]').click()
#     sleep(1)
#     page_source = driver.page_source
#     cinema_tree = etree.HTML(page_source)
#     # cinemaName = cinema_tree.xpath('//*[@class="nav-header navBarTitle"]')[0].text
#     theatres = cinema_tree.xpath('//*[@class="theatre-list"]/div')[1]
#     for theatre in theatres:
#         riqi.append(theatre.xpath('.//li')[0].text.strip())
#         piaofang.append(theatre.xpath('.//li')[1].text)
#         changjunrenci.append(theatre.xpath('.//li')[2].text)
#         danzuopiaofang.append(theatre.xpath('.//li')[3].text)
#     print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '爬取完毕，正写入数据库')
#     for date in range(0, len(riqi)):
#         sql2 = """INSERT INTO cinema_piaofang_maoyanpiaofang(CINEMA_ID, RIQI, PIAOFANG, CHANGJUNRENCI, DANZUOPIAOFANG, UPDATETIME)
#              VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (CienmaID, riqi[date], piaofang[date], changjunrenci[date], danzuopiaofang[date], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         cursor2.execute(sql2)
#         db2.commit()
#     print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '数据库写入成功')
#     driver.close()
# db2.close()



'''
第二版优化，提高运行效率
'''
db2 = pymysql.connect('192.168.3.161', 'python_db', '', 'python_db', charset='utf8')
cursor2 = db2.cursor()
print('开始爬取影院票房数据，已完成', str(min), '家，剩余', str(max - min), '家')
# for num in range(0,1):
# for num in range(0,len(List_Id)):
driver = webdriver.Chrome(executable_path='E:\\PythonProject\\chromedriver.exe')
for num in range(min, max):
    CienmaID = List_CinemaId[num]
    CinemaName = List_CinemaName[num]
    print('总', str(max), '家影院，正在爬取第', str(num + 1), '家影院', CinemaName)
    riqi = []
    piaofang = []
    changjunrenci = []
    danzuopiaofang = []
    CinemaUrl = 'http://piaofang.maoyan.com/company/cinema/' + str(CienmaID)
    driver.get(CinemaUrl)
    sleep(1.5)
    driver.find_element_by_xpath('//*[@id="op-view"]/div[1]/ul/li[4]').click()
    sleep(1)
    page_source = driver.page_source
    cinema_tree = etree.HTML(page_source)
    # cinemaName = cinema_tree.xpath('//*[@class="nav-header navBarTitle"]')[0].text
    theatres = cinema_tree.xpath('//*[@class="theatre-list"]/div')[1]
    for theatre in theatres:
        riqi.append(theatre.xpath('.//li')[0].text.strip())
        piaofang.append(theatre.xpath('.//li')[1].text)
        changjunrenci.append(theatre.xpath('.//li')[2].text)
        danzuopiaofang.append(theatre.xpath('.//li')[3].text)
    print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '爬取完毕，正写入数据库')
    for date in range(0, len(riqi)):
        sql2 = """INSERT INTO cinema_piaofang_maoyanpiaofang(CINEMA_ID, RIQI, PIAOFANG, CHANGJUNRENCI, DANZUOPIAOFANG, UPDATETIME)
             VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (CienmaID, riqi[date], piaofang[date], changjunrenci[date], danzuopiaofang[date], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor2.execute(sql2)
        db2.commit()
    print("%-15s" % '' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '数据库写入成功')
driver.close()
db2.close()