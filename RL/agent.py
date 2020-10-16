import parl
from parl import layers
import numpy as np
import paddle.fluid as fluid

class Agent(parl.Agent):
    def __init__(self, algorithm, obs_dim, act_dim, e_greed=0.1, e_greed_decrement=0):
        '''
        :param algorithm: 之前编写的algorithm类
        :param obs_dim: 状态空间的维度
        :param act_dim: 动作空间的维度
        :param e_greed: 计算回报值的衰减因子
        :param e_greed_decrement: 随着训练逐步收敛，探索的程度逐渐降低
        '''

        # 输入有效值检验
        assert isinstance(obs_dim, int)
        assert isinstance(act_dim, int)
        self.obs_dim = obs_dim
        self.act_dim = act_dim
        super(Agent, self).__init__(algorithm)  # algorithm的构造函数

        self.global_step = 0
        self.update_target_steps = 200 # 每隔200步就将主网络的参数同步到目标网络

        self.e_greed = e_greed
        self.e_greed_decrement = e_greed_decrement

    # 定义计算图
    def build_program(self):
        self.pred_program = fluid.Program()     # 预测用的程序
        self.learn_program = fluid.Program()    # 训练用的程序

        # 在预测程序下申明变量类型
        with fluid.program_guard(self.pred_program):
            obs = layers.data(name="obs", shape=[self.obs_dim], dtype="float32")
            self.value = self.alg.predict(obs)

        # 在训练程序下申明变量类型
        with fluid.program_guard(self.learn_program):
            obs = layers.data(name="obs", shape=[self.obs_dim], dtype="float32")
            action = layers.data(name="act", shape=[1], dtype="int32")
            reward = layers.data(name="reward", shape=[], dtype="float32")
            next_obs = layers.data(name="next_obs", shape=[self.obs_dim], dtype="float32")
            terminal = layers.data(name="terminal", shape=[], dtype="bool")
            self.cost = self.alg.learn(obs, action, reward, next_obs, terminal)

    def sample(self, obs):
        if np.random.uniform(0, 1) < self.e_greed:
            action = np.random.choice(self.act_dim)
        else:
            action = self.predict(obs)
        self.e_greed = max(0.01, self.e_greed - self.e_greed_decrement) # 逐渐降低e_greed直到0.01
        return action

    def predict(self, obs):
        obs = np.expand_dims(obs, axis=0)

        # 运行一次计算图
        pred_Q = self.fluid_executor.run(
            self.pred_program,
            feed={"obs":obs.astype("float32")},
            fetch_list=[self.value]
        )[0]

        pred_Q = np.squeeze(pred_Q, axis=0) # 降低张量阶数
        action = np.argmax(pred_Q)  # 选取最大值对应的索引值
        return action

    def learn(self, obs, act, reward, next_obs, terminal):
        # 每隔update_target_steps步同步一次网络参数
        if self.global_step % self.update_target_steps == 0:
            self.alg.sync_target()
        self.global_step += 1

        act = np.expand_dims(act, -1)
        # 定义输入数据
        feed = {
            "obs":obs.astype("float32"),
            "act":act.astype("int32"),
            "reward":reward,
            "next_obs":next_obs.astype("float32"),
            "terminal":terminal
        }
        cost = self.fluid_executor.run(
            self.learn_program,
            feed=feed,
            fetch_list=[self.cost]
        )[0]
        return cost

if __name__ == "__main__":
    pass