# -*- coding: utf-8 -*-
import random

"""斗地主发牌叫分加倍"""


def shuffle():
    """
    此函数用于洗牌，牌库为列表Deck，其中3-10分别代表3-10四花色的牌
    11代表‘J’牌，12代表‘Q’牌，13代表‘K’牌，14代表‘A’牌，15代表‘2’牌
    16代表‘小王’，17代表‘大王’
    """
    Deck = [3, 3, 3, 3,  # 3
            4, 4, 4, 4,  # 4
            5, 5, 5, 5,  # 5
            6, 6, 6, 6,  # 6
            7, 7, 7, 7,  # 7
            8, 8, 8, 8,  # 8
            9, 9, 9, 9,  # 9
            10, 10, 10, 10,  # 10
            11, 11, 11, 11,  # J
            12, 12, 12, 12,  # Q
            13, 13, 13, 13,  # K
            14, 14, 14, 14,  # A
            15, 15, 15, 15,  # 2
            16,  # 小王
            17]  # 大王
    random.shuffle(Deck)  # 洗牌
    return Deck

def sort(lst):
    '''排序'''
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j] < key:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst

def replace(lst):
    '''此函数是将数字替换成现实中的牌面'''
    while 11 in lst:
        lst[lst.index(11)] = 'J'
    while 12 in lst:
        lst[lst.index(12)] = 'Q'
    while 13 in lst:
        lst[lst.index(13)] = 'K'
    while 14 in lst:
        lst[lst.index(14)] = 'A'
    while 15 in lst:
        lst[lst.index(15)] = '2'
    while 16 in lst:
        lst[lst.index(16)] = '小王'
    while 17 in lst:
        lst[lst.index(17)] = '大王'
    return lst

def anti_replace(lst):
    '''将牌面还原为数字'''
    while '3' in lst:
        lst[lst.index('3')] = 3
    while '4' in lst:
        lst[lst.index('4')] = 4
    while '5' in lst:
        lst[lst.index('5')] = 5
    while '6' in lst:
        lst[lst.index('6')] = 6
    while '7' in lst:
        lst[lst.index('7')] = 7
    while '8' in lst:
        lst[lst.index('8')] = 8
    while '9' in lst:
        lst[lst.index('9')] = 9
    while '10' in lst:
        lst[lst.index('10')] = 10
    while 'J' in lst:
        lst[lst.index('J')] = 11
    while 'Q' in lst:
        lst[lst.index('Q')] = 12
    while 'K' in lst:
        lst[lst.index('K')] = 13
    while 'A' in lst:
        lst[lst.index('A')] = 14
    while '2' in lst:
        lst[lst.index('2')] = 15
    while '小王' in lst:
        lst[lst.index('小王')] = 16
    while '大王' in lst:
        lst[lst.index('大王')] = 17
    return lst

def HoleCards(lst):  # 底牌
    hole_cards = replace(lst)
    return hole_cards

def FirstCards(lst):  # 第一个玩家的17张牌排序
    first_cards = replace(sort(lst))
    print('一号：', first_cards)
    return first_cards

def SecondCards(lst):  # 第二个玩家的17张牌排序
    second_cards = replace(sort(lst))
    print('二号', second_cards)
    return second_cards

def ThirdCards(lst):  # 第三个玩家的17张牌排序
    third_cards = replace(sort(lst))
    print('三号', third_cards)
    return third_cards

def Final(lst, lst1):
    landlord_cards = lst + lst1
    landlord_cards = replace(sort(anti_replace(landlord_cards)))
    print('底牌', lst1)
    print('地主牌：', landlord_cards)

def score(lst):
    score = 0;
    cards = anti_replace(lst)
    #10以上单牌JQKA2小王大王每张加1-7分
    for i in cards:
        if i == 11:
            score += 1
        if i == 12:
            score += 2
        if i == 13:
            score += 3
        if i == 14:
            score += 4
        if i == 15:
            score += 5
        if i == 16:
            score += 6
        if i == 17:
            score += 7
    #炸弹加10分
    bomb = 0
    for j in range(len(cards)):
        if cards[j] == cards[j - 3]:
            bomb += 1
    score += 10 * bomb
    #三条加3分
    triple = 0
    for j in range(len(cards)):
        if cards[j] == cards[j - 2] and cards[j] != cards[j - 3]:
            triple += 1
    score += 3 * triple
    #王炸加20分
    if 16 in cards and 17 in cards:
        score += 20
    return score

def jiaofen(s):
    if s < 25:
        print('不叫', '不抢')
    if s >= 25 and s < 30:
        print('1分', '抢地主')
    if s >= 30 and s < 40:
        print('2分', '抢地主')
    if s >= 40:
        print('3分', '抢地主')

def jiabei(s):
    if s < 40:
        print('不加倍')
    if s >= 40:
        print('加倍')

def main():
    print('-----斗地主发牌叫分加倍,默认一号地主-----\n')
    Deck = shuffle()  # 洗牌
    hole_cards = Deck[-3:]  # 斗地主起始的三张底牌
    first_cards = Deck[:-3:3]
    second_cards = Deck[1:-3:3]
    third_cards = Deck[2:-3:3]

    HoleCards(hole_cards)
    first_cards = FirstCards(first_cards)
    s1 = score(first_cards)
    print('牌力估价：', s1)
    jiaofen(s1), jiabei(s1)

    second_cards = SecondCards(second_cards)
    s2 = score(second_cards)
    print('牌力估价：', s2)
    jiaofen(s2), jiabei(s2)

    third_cards = ThirdCards(third_cards)
    s3 = score(third_cards)
    print('牌力估价：', s3)
    jiaofen(s3), jiabei(s3)

    hole_cards = HoleCards(hole_cards)
    Final(first_cards, HoleCards(hole_cards))
    dizhu_cards = sort(first_cards + anti_replace(hole_cards))
    s4 = score(dizhu_cards)
    print('牌力估价：', s4)
    jiabei(s4)

if __name__ == '__main__':
    main()

