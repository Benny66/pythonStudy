# -*- coding:utf-8 -*-  
import requests
from lxml import etree

import csv
import urllib.request





def get(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    response=requests.get(url, headers=header)
    if response ==  '':
        return
    text=response.content.decode("utf8")#网页的编码方式是“gbk”，经过该操作之后返回的是字符串
    html = etree.HTML(text)
    if html == None:
        print(html)
        return
    content= html.xpath("//div[@class='list_s2_item']/a/strong/text()")#返回的是列表
    if content==None | content == '':
        return
    with open("广东菜谱名称.csv","a",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(content)

def main():
    i=1
    while True:
        if i != 1:
            X='/p'+str(i)+'/'
        else:
            X='/'
        url="http://www.meishij.net/xiaochi/guangdongxiaochi"+ X
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')]
        try:
            print(url)
            result = opener.open(url)#判断url是否有效
            get(url)
            i+=1
        except urllib.error.HTTPError:
            print(url + '=访问页面出错')
            break
    
if __name__ == '__main__':
    main()
