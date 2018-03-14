import pymysql
import requests
import datetime
from selenium import webdriver
from time import sleep
from lxml import etree

# 生成访问抬头信息
headers_PC = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
headers_H5 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

# 判断元素是否存在的公式_第二版，判断是否存在某个元素，返回Ture和False
def isElementExist(self, element):
    flag = True
    element = self.find_elements_by_xpath(element)
    if element == []:
        flag = False
        return flag
    else:
        return flag

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


# 爬取城市影院页面中每一个影院的ID
def get_cinemaUrl(Url):
    # 调用webdriver来启动Chrome浏览器
    driver = webdriver.Chrome(executable_path='E:\\PythonProject\\chromedriver.exe')
    # 使用浏览器来打开Url
    driver.get(Url)
    sleep(3)
    # 使用isElementExist函数，判断页面是否需要点击加载，如果需要则点击加载
    element_flag = isElementExist(driver, ".//*[@class='more']")
    while element_flag:
        driver.find_element_by_id("moreCinema").click()
        sleep(1)
        element_flag = isElementExist(driver, ".//*[@class='more']")
        sleep(1)
    # 解析页面HTML，并抓取指定Xpath位置
    page_source = driver.page_source
    cinema_tree = etree.HTML(page_source)
    city_lis = cinema_tree.xpath('//*[@id="selectedCity"]')[0].text
    city_id = dict_cityNametoId[city_lis]
    cinema_lis = cinema_tree.xpath('//div[@id="pageletCinemalist"]/li')
    # 循环获取影院ID和影院名称，并生成链接
    for cinema_li in cinema_lis:
        cinema_name = cinema_li.xpath('.//span[@class="name"]')[0].text
        cinema_id = cinema_li.xpath('.//span/@data-data')[0].strip('{}').split(':')[1]
        cinema_Url = 'https://dianying.baidu.com/cinema/cinemadetail?cityId=' + str(city_id) + '&cinemaId=' + str(cinema_id)
        # 把城市、影院名称、影院连接打印出来
        # print ('['+city_lis+']',cinema_name, cinemaInformationUrl)
        list_cinemaID.append(cinema_id)
        list_cinemaName.append(cinema_name)
        list_cinemaCity.append(dict_cityIdtoName[y])
        list_cinemaUrl.append(cinema_Url)
        list_timenow.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 关闭调用的程序
    driver.close()



'''
下面是插入多行多字段的事例
'''
# id_list = ['1', '2', '3', '4']
# name_list = ['深圳博纳影院', '深圳皇庭影院', '深圳嘉禾影院', '深圳万达影院']
# city_list = ['深圳', '深圳', '深圳', '深圳']
#
# for i in range(0,4):
#     sql = """INSERT INTO TEST(CINEMA_ID,
#              CINEMA_NAME, CITY)
#              VALUES ('%s', '%s', '%s')"""  % (id_list[i], name_list[i], city_list[i])
#     Connect_Mysql(sql)


'''
爬取百度的城市信息，生成列表
'''
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
dict_cityIdtoName = dict(zip(city_id, city_name))
dict_cityNametoId = dict(zip(city_name, city_id))


'''
根据爬取的城市ID生成链接，并爬取每一页的影院信息，写入数据库
'''
cityNum = 0
for y in city_id[426:440]:
    list_cinemaID = []
    list_cinemaName = []
    list_cinemaCity = []
    list_cinemaUrl = []
    list_timenow = []
    cityUrl = 'http://dianying.baidu.com/cinema?cityId=' + str(y)
    cityNum += 1
    UrlIsError = True
    while UrlIsError:
        try:
            get_cinemaUrl(cityUrl)
        except KeyError:
            driver.close()
            UrlIsError = True
            print('[Error]', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '城市【' + dict_cityIdtoName[y] + '】' + '网页打开异常，正尝试重新爬取...', '\r')
        else:
            UrlIsError = False
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '完成第', str(cityNum).zfill(3), '个城市的爬取：' + dict_cityIdtoName[y])
            for z in range(0, len(list_cinemaID)):
                sql = """INSERT INTO cinemaname_baidu(CINEMA_ID, CINEMA_NAME, CINEMA_CITY, CINEMA_URL, UPDATE_TIME)
                     VALUES ('%s', '%s', '%s', '%s', '%s')""" % (list_cinemaID[z], list_cinemaName[z], list_cinemaCity[z], list_cinemaUrl[z], list_timenow[z])
                Connect_Mysql(sql)