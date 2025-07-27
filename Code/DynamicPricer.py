import numpy as np
from shared import ml_model, price_range
from sklearn.linear_model import LinearRegression


class DynamicPricer:
    """
    实现了基于乘法权重更新 (MWU) 的动态定价机制 (Algorithm 1)。
    """

    def __init__(self, price_range, num_experts, learning_rate_delta):
        """
        初始化动态定价器。

        Args:
            price_range (tuple): 价格的范围 (min_price, max_price)。
            num_experts (int): 专家的数量，即离散化价格点的数量。
            learning_rate_delta (float): MWU算法的学习率 delta。
        """
        # 将价格范围离散化为专家集合
        self.experts = np.linspace(price_range[0], price_range[1], num_experts)

        self.num_experts = num_experts
        self.delta = learning_rate_delta

        # 初始化所有专家的权重为1
        self.weights = np.ones(num_experts)

        # B_max 用于归一化收益
        self.B_max = price_range[1]

    def choose_price(self):
        """
        根据当前权重分布，随机选择一个价格。

        Returns:
            float: 选定的市场价格 p_n。
            int: 选定专家的索引。
        """
        # 计算归一化的概率分布
        probabilities = self.weights / np.sum(self.weights)

        # 根据概率分布随机选择一个专家的索引
        chosen_expert_index = np.random.choice(self.num_experts, p=probabilities)

        # 返回对应的价格
        chosen_price = self.experts[chosen_expert_index]

        return chosen_price, chosen_expert_index

    def update_weights(self, auction_mechanism, X, Y, b_n):
        """
        在一次交易后，更新所有专家的权重。

        Args:
            auction_mechanism (HonestAuction): 用于计算虚拟收益的拍卖机制实例。
            X (np.array): 原始特征数据。
            Y (np.array): 目标预测任务数据。
            b_n (float): 本轮买家的出价。
        """
        virtual_gains = np.zeros(self.num_experts)

        # 为每个专家计算虚拟收益
        for i, expert_price in enumerate(self.experts):
            # 计算如果当时使用 expert_price，会产生的收益
            revenue = auction_mechanism.calculate_revenue(X, Y, expert_price, b_n)

            # 归一化收益
            normalized_gain = revenue / self.B_max
            virtual_gains[i] = normalized_gain

        # 执行乘法权重更新
        # w_{n+1}^i = w_n^i * (1 + delta * g_n^i)
        self.weights = self.weights * (1 + self.delta * virtual_gains)

        # 防止权重过大导致数值不稳定
        if np.sum(self.weights) > 1e6:
            self.weights /= np.sum(self.weights)
