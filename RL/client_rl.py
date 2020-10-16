# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Zhelong Huang
# @File       : client.py
# @Description:

import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from AIAction import AIAction

episode_result_list = []    # 记录每个小局结束时的记录
first_end_agent_count = {
    0 : 0, 1 : 0, 2 : 0, 3 : 0
}      # 统计每个agent出完牌的次数
train = False

class ExampleClient(WebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        self.state = State()               # 获取agent所处环境对象
        self.action = AIAction()        # 获取agent动作决策对象
        self.restCards = None          # 剩余的卡牌
        self.episode_rounds = 0       # 当前小局玩的回合数
        self.agent_pos = None         # agent所处的位置

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    # 两个列表做减法
    def listMinus(self, list1, list2):
        for item in list2:
            if item in list1:
                list1.remove(item)
        return list1

    # 获取奖励值
    # 普通一回合，奖励值=对方剩余卡牌数-己方剩余卡牌数
    # 小局结束， 如果赢了，（AABB）奖励值=1500, (ABAB)奖励值= 1000(ABBA)奖励值=500
    # 输了， (BBAA)奖励值=-1500 (BABA)奖励值=-1000, (BAAB)=-500
    def calculate_reward(self, msg):
        em1 = (self.agent_pos + 1) % 4
        em2 = (self.agent_pos + 3) % 4
        self1 = self.agent_pos
        self2 = (self.agent_pos + 2) % 4

        if msg["stage"] == "play":
            em_rest_card_num = msg["publicInfo"][em1]["rest"] + msg["publicInfo"][em2]["rest"]
            self_rest_card_num = msg["publicInfo"][self1]["rest"] + msg["publicInfo"][self2]["rest"]
            return em_rest_card_num - self_rest_card_num

        elif msg["stage"] == "episodeOver":
            if msg["order"][0] in [self1, self2] and msg["order"][1] in [self1, self2]:
                return 1500
            elif msg["order"][0] in [self1, self2] and msg["order"][2] in [self1, self2]:
                return 1000
            elif msg["order"][0] in [self1, self2] and msg["order"][3] in [self1, self2]:
                return 500
            elif msg["order"][0] in [em1, em2] and msg["order"][1] in [em1, em2]:
                return -1500
            elif msg["order"][0] in [em1, em2] and msg["order"][2] in [em1, em2]:
                return -1000
            elif msg["order"][0] in [em1, em2] and msg["order"][3] in [em1, em2]:
                return -500

    def calculate_observation(self, msg):
        return

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)                                                     # 调用状态对象来解析状态

        # 如果是开头，将我们有的卡牌存下来，并获取座位号
        # message type : dict
        if message["stage"] == "beginning":
            self.restCards = message["handCards"]
            self.agent_pos = message["myPos"]

        # 小局结束，回合数清零，并记录一下结果
        if message["stage"] == "episodeOver":
            global episode_result_list, first_end_agent_count
            self.episode_rounds == 0
            episode_result_list.append(message["order"])     # 保留第一个出完牌的agent
            first_end_agent_count[message["order"][0]] += 1     # 计数器+1


        # 目前存在可选动作列表，代表目前可以打牌
        if "actionList" in message:
            self.restCards = message["handCards"]
            # 回合数+1
            self.episode_rounds += 1
            print("剩余卡牌：", self.restCards)

            # 解析当前state（服务器的message、agent剩余卡牌数量、目前的回合数、位置）
            act_index = self.action.parse(msg=message,
                                          restCards=self.restCards,
                                          episode_rounds=self.episode_rounds,
                                          agent_pos=self.agent_pos)

            # 得到代表打牌动作的三元组
            act_trip = message["actionList"][act_index]
            self.send(json.dumps({"actIndex": act_index}))

        if message["stage"] == "gameResult":
            # 训练模式将结果打印出来
            if train:
                import matplotlib.pyplot as plt
                import pandas as pd

                data_df = pd.DataFrame({
                    "name": ["agent0", "agent1", "agent2", "agent3"],
                    "count": list(first_end_agent_count.values())
                })

                data_df.plot(x="name", y="count", kind="bar", figsize=[12, 7])
                plt.grid(True)
                plt.show()

if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client3')
        ws.connect()
        ws.run_forever()

    except KeyboardInterrupt:
        ws.close()