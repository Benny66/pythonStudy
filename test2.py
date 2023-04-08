#coding:utf-8
import random

guess = ''
while guess not in [0, 1]:
    print('------猜硬币游戏------')
    print('猜一猜硬币是正面还是反面？')
    guess = int(input('“正面”请输入0,“反面”请输入1：'))

# 随机抛硬币，0代表正面，1代表反面
toss = random.randint(0,1) 

if toss != guess:
    print('猜对了！你真棒')
else:
    print('没猜对，你还有一次机会。')
    guess = int(input('再输一次“正面”或“反面”：'))
    if toss != guess:
        print('你终于猜对了！')
    else:
        print('大失败！')