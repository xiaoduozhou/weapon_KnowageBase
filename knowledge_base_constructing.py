import os
from lxml import etree
from bs4 import BeautifulSoup as bs

def get_file(path):
    #path = os.getcwd()
    dirs = os.listdir(path)
    return dirs

def write2triple(subject,predicate,object):
     with open('weaponKB.txt','a',encoding='utf-8') as f:
         f.write(subject+"    "+predicate+"    "+object+"\n")


def theFinalWeapon(father_dir,weapon):
    content = ''
    with open(father_dir,'r',encoding='utf-8') as f:
        if os.path.getsize(father_dir) > 1000:
            for line in f:
                content = content + line
        else:
            return 0
    root = etree.HTML(content)

    #国籍
    country = root.xpath("//span[@class = 'country']/b/a/text()")
    write2triple(weapon,'国籍',country[0])
    print(weapon,'国籍',country[0])##################

    #简介
    try:
        description = root.xpath("//div[@class = 'intron']/div[@class = 'module']/text() | //div[@class = 'intron']/div[@class = 'module']/p/text()")
        write2triple(weapon,'简介',"".join(description).strip().replace("\n", ""))#输入的文本必须要去除空格和回车
        print(weapon,'简介',"".join(description).strip().replace(" ","").replace("\n", ""))########################
    except:
        pass

    #结构信息，使用情况
    try:
        infobox_object = root.xpath("//div[@class = 'info']/div/div[@class = 'otherList'][1]/div[@class='textInfo']/p/text()")
        infobox_predicate = root.xpath("//div[@class = 'info']/div/div[@class = 'otherList'][1]/h3[@class='title_']/text()")
        write2triple(weapon,infobox_predicate[0],"".join(infobox_object).strip().replace("\n", ""))
        print(weapon,infobox_predicate[0],"".join(infobox_object).strip().replace(" ","").replace("\n", ""))####################
    except:
        pass

    #基本数据  dataInfo/ul[1]
    try:
        infobox_object = root.xpath("//div[@class = 'dataInfo']/ul[1]/li/text()")
        infobox_predicate = root.xpath("//div[@class = 'dataInfo']/ul[1]/li/span/text()")
        for predicate,object in zip(infobox_predicate,infobox_object):
            write2triple(weapon,predicate.replace("：",""),object)
            print(weapon,predicate.replace("：",""),object)###############
    except:
        pass

    #技术数据  dataInfo/ul[@class ='dataList']
    try:
        infobox_object = root.xpath("//div[@class = 'dataInfo']/ul[@class='dataList']/li/text() | //div[@class = 'dataInfo']/ul[@class='dataList']/li/b/text()")
        infobox_predicate = root.xpath("//div[@class = 'dataInfo']/ul[@class='dataList']/li/span/text()")
        for predicate,object in zip(infobox_predicate,infobox_object):
            write2triple(weapon,predicate.replace("：",""),object)
            print(weapon,predicate.replace("：",""),object)####################
    except:
        pass




def weaponlist(father_dir,father):
    #print(father_dir,father)
    dirs = get_file(father_dir)
    for weaponName in dirs:
         write2triple(father,'子类',weaponName.replace(".html",""))
         #print(father,'子类',weaponName.replace(".html",""))
         mother_dir = father_dir+"\\"+weaponName
         theFinalWeapon(mother_dir,weaponName.replace(".html",""))

def  weaponclass(father_dir,father):
    dirs = get_file(father_dir)
    for weaponName in dirs:
         write2triple(father,'子类',weaponName)
         mother_dir = father_dir+"\\"+weaponName
         weaponlist(mother_dir,weaponName)


def  start():
    dirs = get_file(os.getcwd()+"\\weapon")
    #print(os.getcwd()+"\\weapon")
    for weaponName in dirs:
        write2triple('武器','子类',weaponName)
        father_dir = os.getcwd()+"\\weapon\\"+weaponName
        weaponclass(father_dir,weaponName)

if __name__ =='__main__':
    start()
