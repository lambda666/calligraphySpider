# _*_ coding:utf8 _*_
from selenium import webdriver
from pyquery import PyQuery as pq
import urllib.request as ur
from urllib.parse import quote
import re
import time

browser=webdriver.Firefox()

#browser.implicitly_wait(10)#等待十秒加载不出来就会抛出异常，10秒内加载出来正常返回

# 打开书法字典网主页
browser.get("http://www.shufazidian.com/")

# 设置查询值
browser.find_element_by_xpath("//form[@name='form1']/input[@id='wd']").send_keys("罗")
browser.find_element_by_xpath("//form[@name='form1']/select[@id='sort']").send_keys("8")

# 模拟点击查询
browser.find_element_by_xpath("//form[@name='form1']/button[@type='submit']").click()

x = browser.find_elements_by_xpath("/html/body/div[3]/div[2]/div[1]/div[3]/div")

i = 0
for xx in x:
    img = xx.find_element_by_xpath('./div/div/a/img')
    src = img.get_attribute('src')
    print(src)
    ur.urlretrieve(src, '%s.jpg'%i)
    i += 1


#time.sleep(1)

text=browser.page_source

browser.close()

html = str(pq(text))

#print(html)
with open('page.html','w', encoding='utf-8') as file_object:
    file_object.write(html)
