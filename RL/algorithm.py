import parl
from parl import layers
import copy
import paddle.fluid as fluid

class DQN(parl.Algorithm):
    def __init__(self, model, act_dim=None, gamma=None, lr=None):
        """
        :param model: 定义前向计算的神经网络
        :param act_dim: 动作空间的维度
        :param gamma: 计算回报值的衰减因子
        :param lr: 学习率
        """

        self.model = model       # 主网络
        self.target_model = copy.deepcopy(model)    # 深拷贝主网络得到目标网络

        # 异常检测
        assert isinstance(act_dim, int)
        assert isinstance(gamma, float)
        assert isinstance(lr, float)
        self.act_dim = act_dim
        self.gamma = gamma
        self.lr = lr

    # 将主网络的参数同步到目标网络上去
    def sync_target(self):
        self.model.sync_weights_to(self.target_model)    # 直接调用parl.model对象的内置方法即可

    # 获取model神经网络的前向计算结果
    def predict(self, obs):
        return self.model.value(obs)

    # 核心的神经网络更新
    def learn(self, obs, action, reward, next_obs, terminal):
        '''
        :param obs: St
        :param action: At
        :param reward: Rt+1
        :param next_obs: St+1
        :param terminal: done, True代表episode结束
        :return: 损失函数的值
        '''

        # 通过目标网络计算得到target_Q的值
        target_Q_tensor = self.target_model.value(next_obs)    # 计算St+1对应的价值向量
        max_Q = layers.reduce_max(target_Q_tensor, dim=1)  # 获取每行的最大值，按dim=1收缩
        max_Q.stop_gradient = True  # 停止梯度更新

        # 由于terminal不是标量，所以不能直接用判断
        terminal = layers.cast(terminal, dtype="float32")
        target_Q = reward + (1.0 - terminal) * self.gamma * max_Q

        # 通过主网络计算得到perdict_Q的值
        predict_Q_tensor = self.model.value(obs)
        # 将action转成one-hot向量，并将每一位都变成浮点数
        action_onehot = layers.one_hot(action, self.act_dim)
        action = layers.cast(action_onehot, dtype="float32")
        # 进行elementwise计算并降低张量阶数
        # 比如 predict_Q_tensor = [[2.3, 5.7, 1.2, 3.9, 1.4],  action_onehot=[[0, 0, 0, 1, 0]
        #                         [2.1, 3.7, 4.5, 6.7, 7.1]]                 [0, 1, 0, 0, 0]]
        # 那么elementwise乘法运算后的结果是 [[0, 0, 0, 3.9, 0]
        #                               [0, 3.7, 0, 0, 0]]
        # 再进行dim=1的reduce_sum操作后的结果是 [3.9, 3.7]
        predict_Q = layers.reduce_sum(layers.elementwise_mul(action_onehot, predict_Q_tensor), dim=1)

        # 得到这个batch每条数据的损失函数值的平均值
        cost = layers.square_error_cost(predict_Q, target_Q)
        cost = layers.reduce_mean(cost)

        # 申明优化器（使用Adam优化器）
        optimizer = fluid.optimizer.Adam(learning_rate=self.lr)
        optimizer.minimize(cost)    # 指定优化目标

        return cost

if __name__ == "__main__":
    pass