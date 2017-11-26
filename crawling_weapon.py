import os
import requests
import re
import bs4
import io
import time
import random
from bs4 import BeautifulSoup as bs
from lxml import etree

def make_dirs(name):
    isExists=os.path.exists(name)
    if not isExists:
        os.makedirs(name)

#获得武器所在的页面
def  get_page(dir_name,name,url):
    lists = [' ' , ':' , '/' , '\\' , '*' , '?' , '>' , '<' , '|' , '"',"\n" ," "]
    for str in lists:
        name = name.replace(str,"")
    dir_name = dir_name+"/"+name
    response = requests.get(url,headers=headers).content.decode('utf-8')
    try:
        with open(dir_name+'.html','w',encoding='utf-8') as f:
            #如果原来的文件小于1K有可能里面是 空 或者 404 error 应该覆盖
            if os.path.getsize(dir_name+'.html') < 1000:
                f.write(response)
    except:
        pass

##歼16
def  get_final_weapon(dir_name,url):
    response = requests.get(url,headers=headers).content.decode('utf-8')
    root = etree.HTML(response)
    herf_list = root.xpath("//div[@class = 'picList']/ul/li/span[@class='pic']/a/@href")
    name_list = root.xpath("//div[@class = 'picList']/ul/li/span[@class='name']/a/text()")
    i = 0
    for name, href in zip(name_list,herf_list):
        #print(name,base_url+href)
        t = random.uniform(1, 3)
        time.sleep(t)

        get_page(dir_name,name,base_url+href)
        print("-----------------"+name)

##战斗机
def get_final_weapon_page_num(dir_name,url):
     orl_url = url
     get_final_weapon(dir_name,url)
     print(dir_name+"   已执行  第 1 页")
     try:
         response = requests.get(url,headers=headers).content.decode('utf-8')
         root = etree.HTML(response)
         list_sum = root.xpath("//div[@class = 'pages']/span/a/@data-maxpage")
         sum = list_sum[0]
         for i in range(2,int(sum)+1):
            url = orl_url + "_0_0_"+ str(i)
            get_final_weapon(dir_name,url)
            print(dir_name+"   已执行"+str(int(sum))+":"+str(i))
     except:
             pass

##飞行器
def get_sub_weapon(dir_name,url):
    response = requests.get(url,headers=headers).content.decode('utf-8')
    root = etree.HTML(response)
    herf_list = root.xpath("//div[@class = 'select']/ul[1]/li[2]/span/a/@href")
    name_list = root.xpath("//div[@class = 'select']/ul[1]/li[2]/span/a/text()")
    for name in name_list:
        make_dirs(dir_name+"/"+name)
    for name, href in zip(name_list,herf_list):
        #print(name,base_url+href)

        t = random.uniform(0, 1)
        time.sleep(t)

        get_final_weapon_page_num(dir_name+"/"+name,base_url+href)
        print("-----------------"+name)

def start(start_url):
    response = requests.get(start_url).content.decode('utf-8')
    root = etree.HTML(response)
    herf_list = root.xpath("//div[contains(@class,'weapOver weapOver')]/a/@href")  #the href of the weapon
    name_list = root.xpath("//div[contains(@class,'weapOver weapOver')]/a/@title") #the name of the weapon
    for name in name_list:
        make_dirs(name)
    i = 0
    for name, href in zip(name_list,herf_list):
        print("====================================总体进度 "+str(len(name_list))+"："+str(i+1)+"")
        print(name,href)
        get_sub_weapon(name,href)
        i =i+1

        t = random.uniform(0, 1)
        time.sleep(t)


if __name__ == '__main__':
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    #header 是浏览器头，伪装浏览器

    proxies = {
  				"http": "211.67.77.1:80",
 				  "https": "61.50.172.139:80",
		}
    #proxies是使用代理IP，防止爬取网站导致IP被封

    base_url = "http://weapon.huanqiu.com"
    start_url = "http://mil.huanqiu.com/"
    start(start_url)
    #get_sub_weapon("飞行器","http://weapon.huanqiu.com/weaponlist/aircraft")

