# -- coding: utf-8 --


import random
import sys
import itertools
import logging
import imp

logging.basicConfig(
    level=logging.INFO,
)

# 配置出牌规则
ALLOW_THREE_ONE = True
ALLOW_THREE_TWO = True
ALLOW_FOUR_TWO = True
ALLOW_JJJJ_KKKK = False  # 规则是否允许 两个炸弹 凑成 一个 四带两对

# 牌面值
# 3  3
# 4  4 ...
# A 14
# 2 15
# 小王 16
# 大王 17

poker_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
             19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
             36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]

poker_mapping = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
    , '10': '10', '11': 'J', '12': 'Q', '13': 'K', '14': 'A', '15': '2', '16': "BlackJoker", '17': "RedJoker"}

id_to_poker = [(0, '3'), (1, '3'), (2, '3'), (3, '3'),
               (4, '4'), (5, '4'), (6, '4'), (7, '4'),
               (8, '5'), (9, '5'), (10, '5'), (11, '5'),
               (12, '6'), (13, '6'), (14, '6'), (15, '6'),
               (16, '7'), (17, '7'), (18, '7'), (19, '7'),
               (20, '8'), (21, '8'), (22, '8'), (23, '8'),
               (24, '9'), (25, '9'), (26, '9'), (27, '9'),
               (28, '10'), (29, '10'), (30, '10'), (31, '10'),
               (32, '11'), (33, '11'), (34, '11'), (35, '11'),
               (36, '12'), (37, '12'), (38, '12'), (39, '12'),
               (40, '13'), (41, '13'), (42, '13'), (43, '13'),
               (44, '14'), (45, '14'), (46, '14'), (47, '14'),
               (48, '15'), (49, '15'), (50, '15'), (51, '15'),
               (52, '16'), (53, '17')]


def card_to_num_list_3to2(cards):
    arr = [0] * 15
    if cards:
        for x in cards:
            arr[int(x) - 3] += 1
    return arr


def num_list_to_cards(nums):
    arr = []
    for idx, val in enumerate(nums):
        for i in range(0, val):
            arr.append(idx + 3)
    return arr


def selectMulti(dic, num):
    arr = []
    for k in dic:
        if dic[k] >= num:
            arr.append(k)
    return arr


def selectMultiNoIn(dic, num, notin):
    arr = selectMulti(dic, num)
    arr = [x for x in arr if x not in notin]
    return arr


# 返回  333 444 555
def findStright(dic, multi, minlen):  # dic      mutli 几顺 1 为普通拖拉机   minlen 拖拉机长度 > 1

    pokers = selectMulti(dic, multi)

    # 去掉 2 跟 大小王
    pokers = sorted([x for x in pokers if x <= 14])

    if len(pokers) < minlen:
        return []

    re = []
    sequence_num = 1
    i = 1
    while i < len(pokers):
        # Only 3-A Can be STRIGHT
        if pokers[i] - pokers[i - 1] == 1:  # curPoker - lastPoker
            sequence_num += 1
            if sequence_num >= minlen:
                j = 0
                while sequence_num - j >= minlen:
                    re.append(sorted(list(range(pokers[i] - (sequence_num - j) + 1, pokers[i] + 1)) * multi))
                    j += 1
        else:
            sequence_num = 1
        i += 1

    return re


# 定义牌型
class COMB_TYPE:
    PASS = '过'
    SINGLE = '单'
    PAIR = '对'
    TRIPLE = '三条'
    TRIPLE_ONE = '三带一'
    TRIPLE_TWO = '三带一对'
    JJJJ_Q_K = '四带二'
    JJJJ_QQ_KK = '四带两对'
    STRIGHT = '顺子'
    DOUBLES = '双顺'
    THREES = '三顺'
    PLANE_ONES = '飞机带单'
    PLANE_TWOS = '飞机带双'
    BOMB = '炸弹'
    KING_PAIR = '王炸'


HAND_PASS = {'type': COMB_TYPE.PASS, 'poker': []}


# 斗地主程序，启动后模拟3个玩家洗牌，抓拍，套路出牌，到最终分出胜负。
class Doudizhu:

    def __init__(self):
        # 定义牌的映射值

        # 本局玩家持有牌数组[[],[],[]]
        # [[3, 5, 6, 6, 6, 7, 7, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 16], [4, 4, 4, 4, 5, 6, 8, 9, 9, 10, 12, 14, 14, 15, 15, 15, 17], [3, 3, 3, 5, 5, 7, 7, 8, 8, 8, 9, 10, 11, 11, 12, 13, 13]
        self.users = [[], [], []]
        # 历史出牌的内容
        self.handout_hist = []
        self.is_end = 'N'

        #
        self.log = []
        self.id = ''
        self.winner = -1
        self.playerIds = []
        self.ai_last = []
        self.playerAiHands = [[], [], []]
        self.playerAiHandsY = [[], [], []]

    def logInfo(self, s):
        logging.info(s)
        self.log.append(s)

    # 洗牌，随机生成54个数的数组，并抽掉一个数
    def xipai(self):
        self.poker_ids = poker_ids[:]
        random.shuffle(self.poker_ids)
        n = random.randint(1, 54)
        b = self.poker_ids[:n]
        c = self.poker_ids[n:]
        self.poker_ids = c + b

    # 发牌，最后留3张，其他分3份
    def fapai(self):
        self.hand_ids_1 = self.poker_ids[:-3:3]
        self.hand_ids_2 = self.poker_ids[1:-3:3]
        self.hand_ids_3 = self.poker_ids[2:-3:3]
        self.dizhu_ids = self.poker_ids[-3:]
        self.hand_ids_1 += self.dizhu_ids
        self.hand_ids_1.sort()
        self.hand_ids_2.sort()
        self.hand_ids_3.sort()

        # 牌面和洗牌id的映射
        zdpai = dict(id_to_poker)
        paistr1 = ''
        for i in range(len(self.hand_ids_1)):
            paistr1 += zdpai[self.hand_ids_1[i]] + ' '
        paistr2 = ''
        for i in range(len(self.hand_ids_2)):
            paistr2 += zdpai[self.hand_ids_2[i]] + ' '
        paistr3 = ''
        for i in range(len(self.hand_ids_3)):
            paistr3 += zdpai[self.hand_ids_3[i]] + ' '
        self.users[0] = ([int(x) for x in paistr1.strip().split(' ')])
        self.users[1] = ([int(x) for x in paistr2.strip().split(' ')])
        self.users[2] = ([int(x) for x in paistr3.strip().split(' ')])

    # 出牌大小比较:comb2是否比comb1大
    def can_comb2_beat_comb1(self, comb1, comb2):
        if comb2['type'] == COMB_TYPE.PASS:
            return False

        if not comb1 or comb1['type'] == COMB_TYPE.PASS:
            return True

        if comb2['type'] == COMB_TYPE.KING_PAIR:
            return True

        if comb1['type'] != comb2['type'] and comb2['type'] == COMB_TYPE.BOMB:
            return True

        # 下面必须同类型， 同张数
        if comb1['type'] == comb2['type'] and len(comb1['poker']) == len(comb2['poker']):
            return comb2['main'] > comb1['main']

        return False

    def oneHandMaxType(self, pokers):
        allhands = self.get_all_hands(pokers)
        found = []
        for hand in allhands:
            if sorted(hand['poker']) == pokers:
                found.append(hand)

        if len(found) == 1:
            return found[0]
        elif len(found) > 1:
            # 直接返回最难匹配的那种
            for hand in found:
                if hand['type'] == COMB_TYPE.THREES:
                    return hand

            big = found[0]
            for hand in found:
                if self.can_comb2_beat_comb1(hand, big):
                    big = hand
            return big

        else:
            return HAND_PASS

    def oneHand(self, pokers, t):
        allhands = self.get_all_hands(pokers)
        for hand in allhands:
            if sorted(hand['poker']) == pokers and hand['type'] == t:
                return hand
        return HAND_PASS

    # 从持有牌中计算所有可以出牌类型的排列组合   从最小开始， 单， 对， 三， 炸， 顺
    def get_all_hands(self, pokers):

        combs = [HAND_PASS]

        if not pokers:  # <type 'list'>: [3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 10, 10, 11, 12, 12, 13, 14, 15, 15, 15]
            return combs

        dic = {}
        for poker in pokers:
            dic[poker] = dic.get(poker, 0) + 1
            # {3: 2, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 10: 2, 11: 1, 12: 2, 13: 1, 14: 1, 15: 3}

        for poker in dic:
            if dic[poker] >= 1:
                # SINGLE
                combs.append({'type': COMB_TYPE.SINGLE, 'main': poker, 'poker': [poker]})
            if dic[poker] >= 2:
                # PAIR
                combs.append({'type': COMB_TYPE.PAIR, 'main': poker, 'poker': [poker] * 2})
            if dic[poker] >= 3:
                # TRIPLE
                combs.append({'type': COMB_TYPE.TRIPLE, 'main': poker, 'poker': [poker] * 3})
                for poker2 in dic:
                    if ALLOW_THREE_ONE and dic[poker2] >= 1 and poker2 != poker:
                        # TRIPLE_ONE
                        combs.append({'type': COMB_TYPE.TRIPLE_ONE, 'main': poker, 'poker': [poker] * 3 + [poker2]})
                    if ALLOW_THREE_TWO and dic[poker2] >= 2 and poker2 != poker:
                        # TRIPLE_TWO
                        combs.append({'type': COMB_TYPE.TRIPLE_TWO, 'main': poker, 'poker': [poker] * 3 + [poker2] * 2})

            if dic[poker] == 4:
                # BOMB
                combs.append({'type': COMB_TYPE.BOMB, 'main': poker, 'poker': [poker] * 4})
                if ALLOW_FOUR_TWO:

                    ones = selectMultiNoIn(dic, 1, [poker])
                    pairs = selectMultiNoIn(dic, 2, [poker])

                    for c in itertools.combinations(ones, 2):
                        combs.append({'type': COMB_TYPE.JJJJ_Q_K, 'main': poker,
                                      'poker': [poker] * 4 + list(c)})

                    for c in itertools.combinations(pairs, 2):
                        if ALLOW_JJJJ_KKKK or c[0] != c[1]:
                            combs.append({'type': COMB_TYPE.JJJJ_QQ_KK, 'main': poker,
                                          'poker': [poker] * 4 + sorted(list(c) * 2)})

        if 16 in pokers and 17 in pokers:
            # KING_PAIR
            combs.append({'type': COMB_TYPE.KING_PAIR, 'poker': [16, 17]})

        # STRIGHT
        stright = findStright(dic, 1, 5)

        for train in stright:
            combs.append({'type': COMB_TYPE.STRIGHT, 'main': train[0],
                          'poker': train})

        # 双顺 3个以上
        doubles = findStright(dic, 2, 3)
        for ds in doubles:
            combs.append({'type': COMB_TYPE.DOUBLES, 'main': ds[0], 'poker': ds})

        # 三顺 2个以上
        threes = findStright(dic, 3, 2)
        for threes in threes:
            combs.append({'type': COMB_TYPE.THREES, 'main': threes[0], 'poker': threes})

            # 单张的 ， 有可能  77778889 放飞机里面去
            poker_clone = pokers[:]
            for x in threes:
                poker_clone.remove(x)
            for c in set(itertools.combinations(poker_clone, int(len(threes) / 3))):
                combs.append({'type': COMB_TYPE.PLANE_ONES, 'main': threes[0],
                              'poker': threes + list(c)})

            pairs = selectMultiNoIn(dic, 2, threes)  # 三顺的JJJQQQ， 剩下 J Q 不可能是对
            for c in set(itertools.combinations(pairs, int(len(threes) / 3))):
                combs.append({'type': COMB_TYPE.PLANE_TWOS, 'main': threes[0],
                              'poker': threes + sorted(list(c) * 2)})

        # 是不是有多种解读    [9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12]
        # for x in combs:
        #     for y in combs:
        #         if x != y and x['poker'] == y['poker']:
        #             print x, y
        #             raise Exception("一个出牌有多种解读")

        return combs

    # 出牌后把出掉的牌从持有牌中剔除，返回剩余的牌
    def make_hand(self, pokers, hand):
        if (hand['type'] == COMB_TYPE.PASS):
            return pokers
        for x in hand['poker']:
            pokers.remove(x)
        return pokers

    # 上游PASS之后，我方主动出牌策略：
    # 循环持有牌的所有出牌可能，优先顺序为3带x，顺子，对子，单牌，炸弹，王炸
    # 同种牌里面，找到最小的出
    def handout_maxnum(self, all_hands):
        firstFindDic = {}
        all_hands_clone = all_hands[:]

        #  简单规则1 先不破炸弹
        bombs = [x for x in all_hands if x['type'] == COMB_TYPE.BOMB]
        todel = []
        for hand in all_hands:
            for bomb in bombs:
                if (bomb['main'] in hand['poker']):
                    todel.append(hand)
                    break
        all_hands = [x for x in all_hands if x not in todel]
        if len(all_hands) == 1:  # 只剩过了
            all_hands = all_hands_clone

        #  出手头各个类型最小的
        for hand in all_hands:
            if firstFindDic.get(hand['type']) is None or self.can_comb2_beat_comb1(hand, firstFindDic[hand['type']]):
                # 测试 出手头最大的
                # if firstFindDic.get(hand['type']) is None or self.can_comb2_beat_comb1(firstFindDic[hand['type']], hand):
                firstFindDic[hand['type']] = hand

        # 倒数第二手出大 简单规则2
        if len(all_hands) <= 3:
            firstFindDic.clear()
            for hand in all_hands:
                if firstFindDic.get(hand['type']) is None or self.can_comb2_beat_comb1(firstFindDic[hand['type']],
                                                                                       hand):
                    firstFindDic[hand['type']] = hand

        # 拆成出牌次数， 越少越好 简单规则3

        prior = [
            COMB_TYPE.PLANE_TWOS,
            COMB_TYPE.PLANE_ONES,

            COMB_TYPE.THREES,
            COMB_TYPE.DOUBLES,

            COMB_TYPE.JJJJ_QQ_KK,

            COMB_TYPE.TRIPLE_ONE,
            COMB_TYPE.TRIPLE_TWO,
            COMB_TYPE.TRIPLE,
            COMB_TYPE.STRIGHT,

            COMB_TYPE.PAIR,
            COMB_TYPE.JJJJ_Q_K,
            COMB_TYPE.SINGLE,

            COMB_TYPE.BOMB,
            COMB_TYPE.KING_PAIR,
            COMB_TYPE.PASS,
        ]

        for p in prior:
            if firstFindDic.get(p):
                return firstFindDic[p]

        self.logInfo('pass ' + str(all_hands))
        return all_hands[0]

    def print_hand(self, hand):
        re = hand['type'] + " "
        if hand.get('poker'):
            re += str([poker_mapping[str(s)] for s in hand.get('poker')])
        return re

    def cur_player_idx(self):
        return (len(self.handout_hist)) % 3

    # 依据上游历史出牌的内容，决定本次  按规则可以 出牌 的内容
    # 这里也可以设计一些规则
    # handout_hist dizhu users
    def canGoHands(self):
        handout_seq = len(self.handout_hist)
        last_handout = HAND_PASS
        if (handout_seq >= 1):
            last_handout = self.handout_hist[handout_seq - 1]
        if (last_handout['type'] == COMB_TYPE.PASS and handout_seq >= 2):
            last_handout = self.handout_hist[handout_seq - 2]

        cur_player = self.cur_player_idx()

        return self.allCanGoHandsByPokeAndLast(self.users[cur_player], last_handout)

    def allCanGoHandsByPokeAndLast(self, pokers, last_handout):

        all_hands = self.get_all_hands(pokers)

        allCanGoHands = []
        # 第一次出牌，或者上游PASS以及上上游PASS, 本次为主动出牌策略
        if last_handout['type'] == COMB_TYPE.PASS:
            # 主动出牌策略
            allCanGoHands = all_hands
        else:
            # 被动出牌策略:找到能大住上次出牌的牌，或者大住上上次出牌的牌
            for hand in all_hands:
                if self.can_comb2_beat_comb1(last_handout, hand):
                    allCanGoHands.append(hand)

        if (HAND_PASS not in allCanGoHands):
            allCanGoHands.insert(0, HAND_PASS)

        return allCanGoHands

    def player_hand_out(self, handout):

        # 打印出牌日志
        handout_seq = len(self.handout_hist)
        cur_player = self.cur_player_idx()

        self.logInfo(" 出牌次序:  " + str(handout_seq))
        user = '农民'
        if cur_player == 0:
            user = '地主'

        try:
            self.logInfo(str(user) + "[" + str(cur_player) + "]手牌: " + ', '.join(
                [poker_mapping[str(x)] for x in self.users[cur_player]]))
        except:
            pass

        self.logInfo(str(user) + "[" + str(cur_player) + "]出牌: " + self.print_hand(handout))
        # 出牌后剔除已出的牌
        self.users[cur_player] = self.make_hand(self.users[cur_player], handout)

        # 记录下来
        self.handout_hist.append(handout)
        # AI记录
        self.ai_last.append(self.handoutToAi(handout))

        # 如果剔除完成后，当前玩家手中无牌，则宣布胜利
        if (len(self.users[cur_player]) == 0):
            self.winner = cur_player
            self.is_end = 'Y'
            self.logInfo(str(user) + "[" + str(cur_player) + "] 胜利！")

    # 依据上游历史出牌的内容，决定本次出牌的内容   handout_seq 表示第几次出牌
    def hand_out(self):
        allCanGoHands = self.canGoHands()
        handout = self.handout_maxnum(allCanGoHands)

        self.player_hand_out(handout)
        return handout

    def play(self):

        for arr in self.users:
            self.logInfo(str(arr))

        self.logInfo("\n---------start-------------\n")

        while self.is_end != 'Y':
            # 打印 所有的矩阵
            self.cardsToAi()
            # 当前手牌
            self.hand_out()
            self.logInfo('')

    def prepare(self):
        self.xipai()
        self.fapai()

    # 开始打牌
    def start(self):
        self.prepare()
        self.play()

    # 上下文数据
    # 1. 自己 当前手牌
    # 2. 自己 上把出牌
    # 3. 上家上把出牌
    # 4. 下家上把出牌
    # 5. 自己历史出牌
    # 6. 上家历史出牌
    # 7. 下家历史出牌
    # 8.根据上家出牌 写 段判断代码来判断当前所有可能的出牌
    def cardsToAi(self):
        cur_player = self.cur_player_idx()
        handout_seq = len(self.handout_hist)
        #
        aiMatrix = []
        aiMatrix.append(card_to_num_list_3to2(self.users[cur_player]))
        aiMatrix.append(self.cardHis(handout_seq - 3))
        aiMatrix.append(self.cardHis(handout_seq - 1))
        aiMatrix.append(self.cardHis(handout_seq - 2))
        aiMatrix.append(self.totalHis(handout_seq - 3))
        aiMatrix.append(self.totalHis(handout_seq - 1))
        aiMatrix.append(self.totalHis(handout_seq - 2))

        aiMatrixNames = ["自己手牌 ", "自己上把 ", "上家上把 ", "下家上把 ", "自己历史 ", "上家历史 ", "下家历史 ", ]
        # for i in range(len(aiMatrix)):
        #     self.logInfo(aiMatrixNames[i]+" : "+str(aiMatrix[i]))

        ai_arr = []
        for arr in aiMatrix:
            ai_arr += arr

        return ai_arr

    def handoutToAi(self, hand):
        return card_to_num_list_3to2(hand.get('poker'))

    def cardHis(self, idx):
        if idx <= 0:
            return [0] * 15
        else:
            return self.ai_last[idx]

    def totalHis(self, idx):
        arr = [0] * 15
        for i in range(idx, -1, -3):
            arr = [a + b for a, b in zip(arr, self.ai_last[i])]
        return arr


if __name__ == "__main__":
    for i in range(1):
        game = Doudizhu()
        game.start()
