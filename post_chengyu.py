import pypinyin
import numpy
import csv

def Transformation(word):
    """
    汉语和拼音相互转换
    返回转换后的拼音
    """
    s=""
    for i in pypinyin.pinyin(word,style=pypinyin.NORMAL):
        s+="".join(i)
    return s


def clean():
    """
    清洗数据,返回的是一个列表，存放的是文件中所有的内容
    """
    path="/Users/shahao/Project/pythonTest/成语大全.csv"
    file = open(path, "r")
    reader = csv.reader(file)
    data = []
    for i in reader:
        # 返回的是列表
        for j in i:
            # 取出列表中的元素，然后在存进一个新的列表
            data.append(j)
    return data

def Matching(word,list_d):
    """
    把输入的成语的的最后一个字转换成的拼音与csv文件中的成语的第一个字的拼音相同的成语匹配出来
    """
    result_list=[]#结果列表
    for i in list_d:
        # print(i[0])
        result = Transformation(i[0])
        if word == result:
            result_list.append(i)
    
    numpy.random.shuffle(result_list)

    if len(result_list) == 0:
        return ""
    return result_list[0]



def main():
    show='一心一意'
    print("一心一意")
    if show == "":
        print("提示：","请输入想要查询的成语")
        return
    else:#这个表示你只要不输入内容就提示，即使是空格也不行
        last = show[-1]
        pinying_1 = Transformation(last)
        list_chengyu = clean()
        result = Matching(pinying_1,list_chengyu)
        print("1111")
        print(result)
    return



if __name__ == '__main__':
    main()