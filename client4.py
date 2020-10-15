# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:

import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from action import Action

from message_gz import check_message

class ExampleClient(WebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        self.state = State()
        self.action = Action()

        self.agent_pos = None

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)                                             # 调用状态对象来解析状态

        if message["stage"] == "beginning":
            self.restCards = message["handCards"]
            self.agent_pos = message["myPos"]

        if "actionList" in message:                                           # 需要做出动作选择时调用动作对象进行解析
            message = check_message(message=message,
                                      pos=self.agent_pos)
            act_index = self.action.parse(message)
            self.send(json.dumps({"actIndex": act_index}))


if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client4')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
