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
            target_dict[item] = target_dict.get(item, 1) + 1
        return target_dict

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
