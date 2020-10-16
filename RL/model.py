import parl
from parl import layers # 此处为paddle.fluid.layers的API

class Model(parl.Model):
    def __init__(self, act_dim):
        hid1_size = 128
        hid2_size = 128
        # 神经网络共有三层:fc(128)+fc(128)+fc(act_dim)
        self.fc1 = layers.fc(size=hid1_size, act="relu")
        self.fc2 = layers.fc(size=hid2_size, act="relu")
        self.fc3 = layers.fc(size=act_dim, act=None)


    def value(self, obs):
        h1 = self.fc1(obs)
        h2 = self.fc2(h1)
        Q = self.fc3(h2)
        return Q

if __name__ == "__main__":
    pass