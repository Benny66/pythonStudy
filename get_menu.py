import requests
import signal
from lxml import etree
import csv
import urllib.request
from db.mysql import MenuDB,session
import json
from datetime import datetime
import re



def signalHandler(signum, frame):
    global stop
    stop = True
    print("终止")

signal.signal(signal.SIGINT, signalHandler)    #读取Ctrl+c信号
stop = False

def getMenuList(url, categoryId):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    response=requests.get(url, headers=header)
    if response ==  '':
        return
    text=response.content.decode("utf8")#网页的编码方式是“gbk”，经过该操作之后返回的是字符串
    html = etree.HTML(text)
    if html == None:
        print(html)
        return

    menuNames= html.xpath("//div[@class='list_s2_item']/a/strong/text()")#返回的是列表
    menuUrls= html.xpath("//div[@class='list_s2_item']/div[@class='imgw']/a[@class='list_s2_item_img']/@href")#返回的是列表
    
    for i in range(len(menuNames)):
        # 是否存在推出信号，全局变量
        if stop:
            print("当前url为:",url,"执行的菜品名称为:",menuNames[i])
            raise ZeroDivisionError("强制退出")
        # 判断菜谱是否存在
        if getMenuInfoFromDB(menuNames[i])  is not None:
            continue
        # 获取到菜谱的详细信息
        image,video,tag,makeTime,mMaterials,aMaterials,step=getMenuInfo(menuUrls[i])
        if image=="" or image == None:
            continue
        now = getNowTime()
        add_menu = MenuDB(
            category_id=categoryId,
            name=menuNames[i],
            image=image,
            video=video,
            tags=tag,
            m_materials=mMaterials,
            a_materials=aMaterials,
            make_time=makeTime,
            step=step,
            created_at=now,
            updated_at=now
        )
        session.add(add_menu)
        session.commit()
    

def getMenuInfo(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    response=requests.get(url, headers=header)
    if response ==  '':
        return
    text=response.content.decode("utf8")#网页的编码方式是“gbk”，经过该操作之后返回的是字符串
    html = etree.HTML(text)
    if html == None:
        print(html)
        return None,None,None,None,None,None,None
    images = html.xpath("//div[@class='recipe_topvideow']/img/@src")#返回的是列表
    if len(images)==0:
        images = html.xpath("//div[@class='recipe_topimgw']/img/@src")#返回的是列表
        if len(images)==0:
            images.append("")
    videos = html.xpath("//div[@class='recipe_topvideow']/video/@src")#返回的是列表
    if len(videos)==0:
        videos.append("")
        

    tags = html.xpath("//div[@class='info2']/div/strong/text()")#返回的是列表
    
    # 主料
    mMaterials = html.xpath("//div[@class='recipe_ingredients']/div[@class='right']")#返回的是列表
    # m_materials2 = html.xpath("//div[@class='recipe_ingredients']/div[@class='right']/strong/text()")#返回的是列表
    
    mMaterialsRe = []
    for item in mMaterials:
        text = ""
        aText = item.xpath('./strong/a/text()')
        if len(aText) != 0:
            text+=aText[0]
        strongText = item.xpath('./strong/text()')
        if len(strongText) != 0:
            text+="【"+strongText[0] + "】"
        mMaterialsRe.append(text)

    # 辅料
    aMaterials = html.xpath("//div[@class='recipe_ingredients recipe_ingredients1']/div[@class='right']")#返回的是列表
    # a_materials2 = html.xpath("//div[@class='recipe_ingredients recipe_ingredients1']/div[@class='right']/strong/text()")#返回的是列表
    
    aMaterialsRe = []
    for item in aMaterials:
        text = ""
        aText = item.xpath('./strong/a/text()')
        if len(aText) != 0:
            text+=aText[0]
        strongText = item.xpath('./strong/text()')
        if len(strongText) != 0:
            text+="【"+strongText[0] + "】"
        aMaterialsRe.append(text)

    # [tag1[0],tag2[0],tag3[0],tag4[0]]
    #步骤
    step_contents = html.xpath("//div[@class='step_content']")#返回的是列表
    stepObjects = []
    i = 0
    for item in step_contents:
        stepObject = {"step":i, "desc":"", "img":""}
        stepTexts = item.xpath('./p/text()')
        if len(stepTexts) != 0:
            stepObject["desc"] = stepTexts[0]

        stepImages = item.xpath('./img/@src')
        if len(stepImages)!=0:
            stepObject["img"] = stepImages[0]
        stepObjects.append(stepObject)
        i+=1
    
    tagStr = ','.join(tags)
    mMaterialsStr = ','.join(mMaterialsRe)
    aMaterialsStr = ','.join(aMaterialsRe)
    if len(stepObjects) != 0:
        stepObjectJson = json.dumps(stepObjects)
    else:
        stepObjectJson = "[]"

    return images[0],videos[0],tagStr,getMenuMakeTime(tags[2]),mMaterialsStr,aMaterialsStr,stepObjectJson

def main():
    i=1
    while True:
        if i != 1:
            X='/p'+str(i)+'/'
        else:
            X='/'
        url="http://www.meishij.net/fenlei/zaocan"+ X
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')]
        try:
            print(url)
            result = opener.open(url)#判断url是否有效
            getMenuList(url, 1)
            i+=1
        except urllib.error.HTTPError:
            print(url + '=访问页面出错')
            break

def getNowTime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%m:%S")

def getMenuMakeTime(data):
    if re.search( "秒",data) is not None:
        result = re.sub( "秒","",data)
        return int(result)
    if re.search("分钟", data ) is not None:
        result = re.sub("分钟", "",data)
        return int(result) * 60
    if re.search( "小时",data) is not None:
        result = re.sub( "小时","", data)
        if result.isdigit():
            return int(result) * 3600
        return 3600
    return 

def getMenuInfoFromDB(name):
    menu = session.query(MenuDB).filter(MenuDB.name == name).first()
    if menu is None:
        return
    return menu.video,menu.tags,menu.m_materials,menu.a_materials,menu.step

def stripArrayStr(array):
    print(array)
    newArray = []
    for i in range(len(array)):
        str = array[i].strip()
        print(str)
        if str == "":
            continue
        newArray.append(str)
    print(newArray)
    return newArray


if __name__ == '__main__':
    main()
    # getMenuInfo("https://www.meishij.net/zuofa/zhengjidangeng_4.html")


