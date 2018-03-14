from selenium import webdriver
from time import sleep
from lxml import etree
import requests

'''
判断元素是否存在的公式_第一版
'''
# def oldisElementExist(self,element):
#     flag = True
#     try:
#         self.find_elements_by_class_name(element)
#         return flag
#     except:
#         flag = False
#         return flag
#
'''
判断元素是否存在的公式_第二版
'''
# def isElementExist(self, element):
#     flag = True
#     element = self.find_elements_by_xpath(element)
#     if element == []:
#         flag = False
#         return flag
#     else:
#         return flag

'''
检查网页打开是否异常
'''

# CityUrl = 'http://dianying.baidu.com/cinema?cityId=320'
# driver = webdriver.Chrome(executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
# # driver = webdriver.PhantomJS()
# driver.get(CityUrl)
# sleep(1)
#
# flag = isElementExist(driver, "more hide")
# driver.close()
#
# print(flag)
#
# x = driver.isElementExist("more hide").text


'''

'''
headers_PC = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
adr_url = 'http://dianying.baidu.com/common/city/citylist?hasLetter=false&isjson=false&channel=&client='
adr = requests.get(adr_url, headers=headers_PC)
all_data = adr.json()
city_data = all_data['data']['all']
#return city_data
city_id = []
for x in city_data:
    city_id.append(x['id'])
print(city_id)
print(len(city_id))