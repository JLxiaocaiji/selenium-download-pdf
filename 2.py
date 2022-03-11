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


def choose():
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//div[@class='dropdown']//a[@class='btn btn-default c-selectex-btn dropdown-btn']//span[@class='c-selectex-btn-text search-select']").click()

    key = input("请选择搜索方式：输入1：仅标题；输入2：仅正文 ; 输入3：标题+正文。别输错ha:" )
    if (key == '1'):
        print('搜索标题')
        driver.find_element_by_xpath("//div[@class='dropdown open']//a[@title='标题']").click()
    elif (key == '2'):
        print('搜索正文')
        driver.find_element_by_xpath("//div[@class='dropdown open']//a[@title='正文']").click()
    elif (key == '3'):
        print('搜索标题+正文')
        driver.find_element_by_xpath("//div[@class='dropdown open']//a[@title='标题+正文']").click()
    else:
        print('???  是 1||2||3   <(￣︶￣)↗[GO!]')
        return choose()
    driver.find_element_by_xpath("//div[@class='search-wrap sh-searchhint-container']/button[@class='search-btn']").click()
    print('(o゜▽゜)o☆[BINGO!]')

# 获取搜索字段 + url 地址
def getUrl():
    global keyword
    keyword = input("请输入搜索关键词：")            # 新租赁准则
    target = quote(keyword)
    print(f"\n{'其url编码为：'+target}\n")
    # return 'http://www.szse.cn/application/search/index.html?keyword='+target
    return 'http://www.szse.cn/application/search/index.html?keyword='+target

# 获取current子页面 所有 url 和 title
def getParams():
    driver.implicitly_wait(30)       # 隐式等待
    total1 = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath("//div[@class='page-num']").text)
    # total1 = driver.find_element_by_id("countStr").text  # 总数及单页面数
    print(total1)

    # list 操作
    list = driver.find_element_by_xpath("//div[@class='article-search-result']")         # 没啥用？
    item = list.find_elements_by_xpath("//a[@class='text ellipsis pdf']")         # 找到 <a>
    add = list.find_elements_by_xpath("//p[@class='item-content ellipsis']")        # p

    for i in range(0,len(item)):
        url = item[i].get_attribute('href')                     # 找到 url
        title = item[i].text
        num = re.findall(r'\d{6}',add[i].text)
        print('正在下载:'+title)
        print(url)
        print('证券代码：'+str(num))
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
        # './租赁准则\\*ST华塑：关于执行新租赁准则并变更相应会计政策的公告.pdf'
        title1 = re.sub('\*','',title)
        with open(os.path.join(r'./' + keyword + './', title1 + '.pdf'), 'wb') as f:
            f.write(pdf.content)

if __name__ == '__main__':
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

    choose()

    time.sleep(5)                                             # 搜索时间太长就需强制等待sleep
    # driver.implicitly_wait(10)                                 #一开始就是0隐式等待
    # total = WebDriverWait(driver, 505).until(lambda x: x.find_element_by_id("dnum").text)  # 一开哦是就是0 太坑了
    total = driver.find_element_by_xpath("//span[@class='keyword']//span[@class='size']").text   # 总数
    all = re.sub(r'\D','',total)
    print('总数为：'+all)

    #  总控制
    if (int(all)) < 10:
        # try:
        getParams()
    else:
    # 先对第一页
        getParams()
        time.sleep(5)
        for i in range(1,int(int(all)/20)+1):
            driver.find_element_by_xpath("//div[@class='paginator']//li[@class='next']").click()  # 点击进入下一页
            time.sleep(10)
            getParams()

    #  *************************要记得清除缓存 driver.delete_all_cookies()






