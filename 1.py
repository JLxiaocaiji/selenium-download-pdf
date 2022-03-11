import json
import requests
from urllib import request
import re
import os
import random
import time
from urllib.parse import quote
from selenium import webdriver
from selenium .webdriver .common .keys import  Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller


# 获取搜索字段 + url 地址
def getUrl():
    global keyword
    keyword = input("请输入搜索关键词：")            # 新租赁准则
    target = quote(keyword)
    print(f"\n{'其url编码为：'+target}\n")
    return 'http://www.sse.com.cn/home/search/?webswd='+target

def ctrl_f():
    time.sleep(5)
    # driver.find_element_by_tag_name('embed').send_keys(Keys.CONTROL, "a")  # selenium 实现不了
    # ActionChains(driver).key_down(Keys.CONTROL).key_down('a').perform() 也不行
    keyboard = Controller()
    keyboard.press(Key.ctrl.value)  # windows下使用
    keyboard.press('f')
    keyboard.release('f')
    keyboard.release(Key.ctrl.value)
    a = 'qw'
    keyboard.type(a)


# 获取current子页面 所有 url 和 title
def getParams():
    driver.implicitly_wait(6)       # 隐式等待
    total1 = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id("countStr").text)
    # total1 = driver.find_element_by_id("countStr").text  # 总数及单页面数
    print(total1)

    # list 操作
    list = driver.find_element_by_id('sse_query_list')         # 找到 dd
    item = list.find_elements_by_xpath('//dd//a')         # 找到 <a>
    add = list.find_elements_by_xpath('//dd//p')        # p

    for i in range(0,len(item)):
        url = item[i].get_attribute('href')                     # 找到 url
        title = item[i].get_attribute('title')
        num = re.findall(r'\d{6}',add[i].text)
        print('正在下载:'+title)
        print((url))
        print('公司代码：'+str(num))
        download_pdf(url, title,num)

# 下载
def download_pdf(url,title,num):
    pdf = requests.get(url)
    if os.path.exists('./'+keyword+'/'+ title + '.pdf'):
        # 中国中金财富证券有限公司2022年面向专业投资者公开发行公司债券（第一期）募集说明书
        if len(num)!=0:
            with open(os.path.join('./'+keyword, title+ num[0] + '.pdf'), 'wb') as f:
                f.write(pdf.content)
        elif len(num)!=0 and (os.path.exists('./'+keyword+'/'+ title + num[0]+'.pdf')):
            with open(os.path.join('./'+keyword, title+ num[0]+str(random.randint(1,5)) + '.pdf'), 'wb') as f:
                f.write(pdf.content)
        else :
            with open(os.path.join('./'+keyword, title+str(random.randint(1,5)) + '.pdf'), 'wb') as f:
                f.write(pdf.content)
    else:
        with open(os.path.join('./'+keyword, title + '.pdf'), 'wb') as f:
            f.write(pdf.content)

if __name__ == '__main__':
    # time.sleep(random.uniform(1, 3))
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'sia.sseinfo.com',
        # 'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }

    url = getUrl()          # 新租赁准则
    os.mkdir('./'+keyword+'/')
    chrome_driver = './chromedriver.exe'  # chromedriver的文件位置
    driver = webdriver.Chrome(executable_path=chrome_driver)     # 通过 chromedriver模拟打开
    driver.get(url)
    time.sleep(10)                                             # 搜索时间太长就需强制等待sleep
    # driver.implicitly_wait(10)                                 #一开始就是0隐式等待
    # total = WebDriverWait(driver, 505).until(lambda x: x.find_element_by_id("dnum").text)  # 一开哦是就是0 太坑了
    total = driver.find_element_by_id("dnum").text   # 总数
    print('总数为：'+total)

    #  总控制
    if (int(total)) < 10:
        # try:
        getParams()
    else:
    # 先对第一页
        getParams()
        for i in range(1,int(int(total)/10)+1):
            driver.find_element_by_class_name('nextPage').click()  # 点击进入下一页
            getParams()

    #  *************************要记得清除缓存 driver.delete_all_cookies()






