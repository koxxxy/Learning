import re
import requests
import os
import time
from selenium import webdriver
from time import sleep
from lxml import etree
from bs4 import BeautifulSoup as bs

headers_PC = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
headers_H5 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

def get_cinema_html(url):
    req = requests.get(url,headers = headers_PC)
    html = req.text
    #print(html)
    return html

# 爬取百度电影的城市，并转换为字典
def cityname_to_cityid():
    adr_url = 'http://dianying.baidu.com/common/city/citylist?hasLetter=false&isjson=false&channel=&client='
    adr = requests.get(adr_url, headers=headers_PC)
    all_data = adr.json()
    city_data = all_data['data']['all']
    #return city_data
    city_id = []
    city_name = []
    for x in city_data:
        city_id.append(x['id'])
    for y in city_data:
        city_name.append(y['name'])
    city_dict = dict(zip(city_name,city_id))
    return city_dict

# 爬取百度电影的城市，并转换为字典
def cityid_to_cityname():
    adr_url = 'http://dianying.baidu.com/common/city/citylist?hasLetter=false&isjson=false&channel=&client='
    adr = requests.get(adr_url, headers=headers_PC)
    all_data = adr.json()
    city_data = all_data['data']['all']
    #return city_data
    city_id = []
    city_name = []
    for x in city_data:
        city_id.append(x['id'])
    for y in city_data:
        city_name.append(y['name'])
    city_dict = dict(zip(city_id,city_name))
    return city_dict

def cityId_list():
    adr_url = 'http://dianying.baidu.com/common/city/citylist?hasLetter=false&isjson=false&channel=&client='
    adr = requests.get(adr_url, headers=headers_PC)
    all_data = adr.json()
    city_data = all_data['data']['all']
    #return city_data
    city_id = []
    for x in city_data:
        city_id.append(x['id'])
    return city_id

# 判断元素是否存在的公式_第二版，判断是否存在某个元素，返回Ture和False
def isElementExist(self, element):
    flag = True
    element = self.find_elements_by_xpath(element)
    if element == []:
        flag = False
        return flag
    else:
        return flag

# 通过城市影院列表(CityUrl)获取所有影院ID
cinemaId_dict = {}

def get_cinema_id(Url):
    # 打开cityurl.txt文件（如果没有则自动新建）
    CinemaUrlTxt = open('cinemaurl.txt', 'a')
    # 调用webdriver来启动Chrome浏览器
    driver = webdriver.Chrome(executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
    #driver = webdriver.PhantomJS()
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
    city_id = CityDict_NAMEtoID[city_lis]
    cinema_lis = cinema_tree.xpath('//div[@id="pageletCinemalist"]/li')
    # 循环获取影院ID和影院名称，并生成链接
    for cinema_li in cinema_lis:
        cinema_name = cinema_li.xpath('.//span[@class="name"]')[0].text
        cinema_id = cinema_li.xpath('.//span/@data-data')[0].strip('{}').split(':')[1]
        cinemaInformationUrl = 'https://dianying.baidu.com/cinema/cinemadetail?cityId=' + str(city_id) + '&cinemaId=' + str(cinema_id)
        # 把城市、影院名称、影院连接打印出来
        # print ('['+city_lis+']',cinema_name, cinemaInformationUrl)
        # 把影院连接写入cinema_url列表里
        cinema_url.append(cinemaInformationUrl)
        # 把影院连接写入cinemaurl.txt文件里
        CinemaUrlTxt.write(cinemaInformationUrl + '\r')
        # 把影院ID、影院名字写入cinemaId_dict字典里
        cinemaId_dict[cinema_id] = cinema_name
    # 关闭调用的程序
    driver.close()
    # 关闭cinemaurl.txt文件
    CinemaUrlTxt.close()
    # 返回字典文件
    return cinemaId_dict

# print(get_cinema_id('http://dianying.baidu.com/cinema?cityId=320'))


# 判断是否存在储存文件，如果有则删除
if os.path.exists('cinemaurl.txt'):
    os.remove('cinemaurl.txt')
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),'已删除之前爬取的文件')
    print('爬取结果储存在cinemaurl.txt文件内' + '\r' + '正在开始爬取影院地址...')
else:
    ...

# 生成城市字典，用于后期翻译ciytid
CityDict_IDtoNAME = cityid_to_cityname()
CityDict_NAMEtoID = cityname_to_cityid()

'''
【使用for循环生成城市列表】v1.0
使用for来爬取所有城市
由于网页存在一定几率展示不全
写了一个try判断KeyError错误，并重新执行
'''
# cinema_url = []
# num = 0
# for i in cityId_list():
#     num += 1
#     try:
#         city_url = 'http://dianying.baidu.com/cinema?cityId=' + str(i)
#         get_cinema_id(city_url)
#     except KeyError:
#         print('*' * 20)
#         print('[Error]', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '城市【' + CityDict_IDtoNAME[i] + '】' + '网页打开异常，正尝试重新爬取...', '\r')
#         print('*' * 20)
#         get_cinema_id(city_url)
#         print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '完成第', str(num).zfill(3), '个城市的爬取：' + CityDict_IDtoNAME[i])
#     else:
#         print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '完成第', str(num).zfill(3), '个城市的爬取：' + CityDict_IDtoNAME[i])



'''
【使用for循环生成城市列表】v1.1
使用for来爬取所有城市
由于网页存在一定几率展示不全，且可能多次打开失败（改善点）
新增了while判断，只要发生展示不全的情况，就一直循环打开
'''
cinema_url = []
num = 0
for i in cityId_list():
    city_url = 'http://dianying.baidu.com/cinema?cityId=' + str(i)
    num += 1
    UrlIsError = True
    while UrlIsError:
        try:
            get_cinema_id(city_url)
        except KeyError:
            UrlIsError = True
            driver.close()
            print('*' * 20)
            print('[Error]', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '城市【' + CityDict_IDtoNAME[i] + '】' + '网页打开异常，正尝试重新爬取...', '\r')
            print('*' * 20)
        else:
            UrlIsError = False
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '完成第', str(num).zfill(3), '个城市的爬取：' + CityDict_IDtoNAME[i])