# -*- coding: utf-8 -*-
# @Time       : 2020/10/14 19:02
# @Author     : Zhelong Huang
# @File       : AIAction.py
# @Description: ai动作类

from random import randint

# 中英文对照表
ENG2CH = {
    "Single": "单张",
    "Pair": "对子",
    "Trips": "三张",
    "ThreePair": "三连对",
    "ThreeWithTwo": "三带二",
    "TwoTrips": "钢板",
    "Straight": "顺子",
    "StraightFlush": "同花顺",
    "Bomb": "炸弹",
    "PASS": "过"
}

# 根据牌的类型给出其映射序号
card_type_mapping = {
    "Single": 0,
    "Pair": 1,
    "Trips": 2,
    "ThreePair": 3,
    "ThreeWithTwo": 4,
    "TwoTrips": 5,
    "Straight": 6,
    "Bomb": 7,
    "StraightFlush": 8,
    "PASS": 9
}

# 我们认为的大牌型
big_type_cards = [
    "Straight", "Bomb", "StraightFlush"
]

# 牌到点数的映射
card2num = {
    "SA":1,"HA":1,"CA":1,"DA":1,
    "S2":2,"H2":2,"C2":2,"D2":2,
    "S3":3,"H3":3,"C3":3,"D3":3,
    "S4":4,"H4":4,"C4":4,"D4":4,
    "S5":5,"H5":5,"C5":5,"D5":5,
    "S6":6,"H6":6,"C6":6,"D6":6,
    "S7":7,"H7":7,"C7":7,"D7":7,
    "S8":8,"H8":8,"C8":8,"D8":8,
    "S9":9,"H9":9,"C9":9,"D9":9,
    "ST":10,"HT":10,"CT":10,"DT":10,
    "SJ":11,"HJ":11,"CJ":11,"DJ":11,
    "SQ":12,"HQ":12,"CQ":12,"DQ":12,
    "SK":13,"HK":13,"CK":13,"DK":13,
    "SB":14,       #小王映射成14，大王映射成15
    "HR":15,
    "PASS":0       #PASS 映射成0
}

class AIAction(object):
    def __init__(self):
        self.actionList = []               # 当前的动作列表
        self.act_range = -1              # 动作索引范围
        self.restCards = []               # agent剩余手牌
        self.starting_threshold = 5  # 开局阈值，在该值之前AI认为是“刚刚开局”
        self.episode_rounds = 0       # 回合数
        self.agent_pos = None         # 位置

    # 统计列表中的词频，并返回字典
    def count(self, list):
        target_dict = {}
        for item in list:
            item = card2num[item]
            target_dict[item] = target_dict.get(item, 1) + 1
        return target_dict

    # 判断选中的卡牌动作是否拆牌
    def splitCards(self, msg, choose_card_trips, rest_cards):
        """
        :param msg: 全局信息
        :param choose_card_trips: agent选择的卡牌三元组
        :param rest_cards: agent剩余卡牌
        :return:
        """
        card_type = choose_card_trips[0]
        cards_num = choose_card_trips[1]
        cards = choose_card_trips[2]

        card_count = self.count(rest_cards)     # 获取剩余卡牌的各点数卡牌数量
        # 判断卡牌类型
        if card_type == "Single":
            count = 1
        elif card_type == "Pair":
            count = 2
        elif card_type == "Trips":
            count = 3

        cur_card_num = card2num[cards[0]]
        if (cur_card_num == 1 or cur_card_num == int(msg["curRank"])) and card_count[card2num[cards[0]]] == 3 and (count == 1 or count == 2):
            flag = True

        if card_count[card2num[cards[0]]] == count:     # 如果卡牌数和剩余数量相等，则没有拆牌
            flag = False
        else:
            flag = True

        return flag


    # 策略算法预测
    def strategy_predict(self, msg):
        if msg["indexRange"] == 0:      # 别无选择
            return 0

        # 接牌
        if self.actionList[0][0] == "PASS":
            if msg["greaterPos"] == (self.agent_pos + 2) % 4:     # 如果最大牌是队友出的
                return self.greaterPosIsFriendStrategy(msg)
            else:                                                                               # 如果最大牌是对手出的
                return self.greaterPosIsOpponentStrategy(msg)

        # 出牌
        else:
            if self.episode_rounds <= self.starting_threshold:        # 大局出牌
                return self.smallRoundsPlayOutStrategy(msg)
            else:
                return self.bigRoundsPlayOutStrategy(msg)             # 小局出牌

    # 点数最大是队友出的策略
    def greaterPosIsFriendStrategy(self, msg):
        if msg["greaterAction"][0] in big_type_cards:       # 队友出的牌型属于大牌
            return 0            # 返回PASS
        else:                                                                        # 队友出的牌型属于小牌
            return 1            # 返回剩余卡牌中最小的那个

    # 点数最大是对手出的策略
    def greaterPosIsOpponentStrategy(self, msg):
        if self.episode_rounds <= self.starting_threshold:      # 回合数较小
            if msg["actionList"][1] in big_type_cards:          # agent能选的只有大牌
                return 0        # 返回PASS
            else:                                                                     # agent能选的有小牌
                return 1        # 返回剩余卡牌中最小的那个
        else:                                                                              # 回合数较大
            return 1

    # 出牌时，回合数较小的策略
    def smallRoundsPlayOutStrategy(self, msg):
        return 0

    # 出牌时，回合数较大的策略
    def bigRoundsPlayOutStrategy(self, msg):
        return 0

    def parse(self, msg, restCards, episode_rounds, agent_pos):
        self.restCards = restCards
        self.episode_rounds = episode_rounds
        self.agent_pos = agent_pos
        # 获取message中的内容
        self.actionList = msg["actionList"]
        self.act_range = msg["indexRange"]

        # 根据所选策略做出判断
        action_index = self.strategy_predict(msg)

        print(self.actionList)          # 打印动作列表
        print("-" * 20)
        print("目前回合数：{}\t可选动作范围为：0至{}\tAI认为应该选择{}".format(
            self.episode_rounds, self.act_range, action_index
        ))

        #action_index = int(input("你认为应该的动作索引："))

        return action_index
