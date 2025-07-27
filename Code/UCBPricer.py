import numpy as np
import math
from shared import ml_model, price_range


class UCBPricer:
    """
    实现了基于置信上界 (UCB) 的动态定价机制
    """

    def __init__(self, price_range, num_experts, confidence_c=2.0):
        """
        初始化 UCB 定价器

        Args:
            price_range (tuple): 价格的范围 (min_price, max_price)
            num_experts (int): 专家的数量，即离散化价格点的数量
            confidence_c (float): 控制探索程度的置信度参数
        """
        self.experts = np.linspace(price_range[0], price_range[1], num_experts)
        self.num_experts = num_experts
        self.c = confidence_c

        # 初始化每个专家的统计数据
        self.counts = np.zeros(num_experts)  # 每个价格被选择的次数
        self.values = np.zeros(num_experts)  # 每个价格的平均收益
        self.total_rounds = 0

    def choose_price(self):
        """
        根据 UCB 规则选择一个价格

        Returns:
            float: 选定的市场价格 p_n
            int: 选定专家的索引
        """
        self.total_rounds += 1

        # 优先选择从未被选过的专家（价格）
        for i in range(self.num_experts):
            if self.counts[i] == 0:
                return self.experts[i], i

        # 计算所有专家的 UCB 值
        ucb_values = np.zeros(self.num_experts)
        for i in range(self.num_experts):
            average_reward = self.values[i]
            exploration_bonus = math.sqrt(
                (self.c * math.log(self.total_rounds)) / self.counts[i]
            )
            ucb_values[i] = average_reward + exploration_bonus

        # 选择 UCB 值最高的专家
        chosen_expert_index = np.argmax(ucb_values)
        chosen_price = self.experts[chosen_expert_index]

        return float(chosen_price), chosen_expert_index

    def update_stats(self, chosen_expert_index, reward):
        """
        在一次交易后，更新被选中专家的统计数据

        Args:
            chosen_expert_index (int): 被选中专家的索引
            reward (float): 从该价格获得的实际收益
        """
        # 更新被选中价格的计数
        self.counts[chosen_expert_index] += 1
        n = self.counts[chosen_expert_index]

        # 增量式更新平均收益
        old_value = self.values[chosen_expert_index]
        new_value = ((n - 1) / n) * old_value + (1 / n) * reward
        self.values[chosen_expert_index] = new_value
