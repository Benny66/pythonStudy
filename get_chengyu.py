# -*- coding:utf-8 -*-  
import requests
from lxml import etree

import csv
import urllib.request


def get(url):
    response=requests.get(url)
    text=response.content.decode("gbk")#网页的编码方式是“gbk”，经过该操作之后返回的是字符串
    html = etree.HTML(text)
    content= html.xpath("//div[@class='listw']/ul/li//text()")#返回的是列表
    with open("成语大全.csv","a",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(content)
    # with open("chengyu.txt", "a")as f:
    #     for i in content:
    #         f.write(i)
    #         f.write(" ")
def main():
    start_list=["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","Q","R","S","T","W","X","Y","Z"]
    for j in start_list:
        i=1
        while True:
            X=str(i)
            url="http://chengyu.t086.com/list/"+ j +"_"+X+".html"
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')]
            try:
                opener.open(url)#判断url是否有效
                get(url)
                i+=1
            except urllib.error.HTTPError:
                print(url + '=访问页面出错')
                break
if __name__ == '__main__':
    main()

