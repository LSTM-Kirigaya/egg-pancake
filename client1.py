# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:

import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from AIAction import AIAction

class ExampleClient(WebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        self.state = State()
        self.action = AIAction()
        self.restCards = None          # 剩余的卡牌
        self.episode_play_nums = 0  # 当前小局玩的次数

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    # 两个列表做减法
    def listMinus(self, list1, list2):
        for item in list2:
            list1.remove(item)
        return list1

    # 输入动作三元组来更新剩余卡片
    def updateRestCards(self, act_trip):
        # 牌型、点数、卡牌
        card_type, card_num, cards = act_trip
        if card_type == "PASS":             # 过
            pass
        elif card_type == "tribute":        # 进贡
            self.listMinus(self.restCards, cards)
        elif card_type == "back":           # 还贡
            self.restCards += cards
        else:                                            # 其余情况：正常出牌
            self.listMinus(self.restCards, cards)


    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)                                             # 调用状态对象来解析状态
        # message type : dict
        if message["stage"] == "beginning":                            # 如果是开头，将我们有的卡牌存下来
            self.restCards = message["handCards"]

        if "actionList" in message:                     # 目前存在actionList，代表目前可以打牌
            print("剩余卡牌：", self.restCards)
            act_index = self.action.parse(message, self.restCards)

            # 得到代表打牌动作的三元组
            act_trip = message["actionList"][act_index]
            # 更新手牌
            self.updateRestCards(act_trip)

            self.send(json.dumps({"actIndex": act_index}))


if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client1')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()