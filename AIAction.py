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

class AIAction(object):
    def __init__(self):
        self.actionList = []               # 当前的动作列表
        self.act_range = -1              # 动作索引范围
        self.restCards = []               # agent剩余手牌
        self.starting_threshold = 5  # 开局阈值，在该值之前AI认为是“刚刚开局”


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

        if self.actionList[0][0] == "PASS":     # 接牌
            pass


        else:                                                       # 出牌
            pass
        # 开始几局不打打牌


        # 选择card_type_mapping映射中最小的那个牌型
        # 选择选择牌型中数量最少的那个





    def parse(self, msg, restCards):
        self.restCards = restCards
        # 获取message中的内容
        self.actionList = msg["actionList"]
        self.act_range = msg["indexRange"]

        # 根据所选策略做出判断
        action_index = self.strategy_predict(msg)

        print(self.actionList)          # 打印动作列表
        print("可选动作范围为：0至{}， AI认为应该选择{}".format(self.act_range, action_index))
        action_index = input("你认为应该的动作索引：")

        return action_index
