import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from shared import ml_model, price_range


class RevenueDivider:
    """
    实现了基于Shapley值的收益分配机制，包括近似算法和对复制鲁棒的算法
    """

    def __init__(self, ml_model, gain_function):
        """
        初始化收益分配器

        Args:
            ml_model: 一个遵循 scikit-learn API 的机器学习模型实例
            gain_function: 一个函数，输入 (y_true, y_pred)，输出预测增益 G
        """
        self.ml_model = ml_model
        self.gain_function = gain_function

    def _get_gain_for_subset(self, X_subset, Y):
        """
        辅助函数：为给定的特征子集计算预测增益
        """
        if X_subset.shape == 0:  # 如果子集为空
            return 0.0

        X_train = X_subset.T
        y_train = Y

        self.ml_model.fit(X_train, y_train)
        y_pred = self.ml_model.predict(X_train)
        return self.gain_function(y_train, y_pred)

    def shapley_approx(self, X, Y, K):
        """
        近似Shapley值 (Algorithm 2: SHAPLEY-APPROX)

        Args:
            X (np.array): 所有卖家的特征数据 (M, T)
            Y (np.array): 目标预测任务数据 (T,)
            K (int): 蒙特卡洛采样的迭代次数

        Returns:
            np.array: 每个卖家的近似Shapley值 (M,)
        """
        M, T = X.shape
        shapley_values = np.zeros(M)

        for _ in range(K):
            # 随机生成一个特征排列
            permutation = np.random.permutation(M)

            # 计算全集增益，用于最后一个特征的边际贡献计算
            gain_full_set = self._get_gain_for_subset(X, Y)

            # 初始化前驱子集的增益
            gain_predecessors = 0.0

            for i in range(M):
                feature_idx = permutation[i]

                # 获取当前特征之前的所有特征
                predecessor_indices = permutation[:i]

                # 计算加入当前特征后的增益
                current_subset_indices = np.append(predecessor_indices, feature_idx)
                gain_current = self._get_gain_for_subset(X[current_subset_indices], Y)

                # 计算边际贡献
                marginal_contribution = gain_current - gain_predecessors
                shapley_values[feature_idx] += marginal_contribution

                # 更新前驱子集的增益
                gain_predecessors = gain_current

        # 取平均值
        shapley_values /= K
        return shapley_values

    def shapley_robust(self, X, Y, K, lambda_param=np.log(2)):
        """
        对复制鲁棒的Shapley值分配 (Algorithm 3: SHAPLEY-ROBUST)

        Args:
            X (np.array): 所有卖家的特征数据 (M, T)
            Y (np.array): 目标预测任务数据 (T,)
            K (int): 蒙特卡洛采样的迭代次数
            lambda_param (float): 指数惩罚项的强度参数

        Returns:
            np.array: 每个卖家的鲁棒Shapley值 (M,)
        """
        # 1. 计算近似Shapley值
        approx_shapley = self.shapley_approx(X, Y, K)

        M, T = X.shape
        robust_shapley = np.zeros(M)

        # 计算所有特征之间的余弦相似度矩阵
        # X shape is (M, T), cosine_similarity expects (n_samples, n_features)
        similarity_matrix = cosine_similarity(X)

        # 2. 应用指数惩罚
        for m in range(M):
            # 计算特征 m 与所有其他特征的总相似度
            # similarity_matrix[m] 是 m 与所有特征的相似度向量
            # np.sum(...) - 1 是因为要排除与自身的相似度（为1）
            total_similarity = np.sum(similarity_matrix[m]) - 1

            # 计算惩罚因子
            penalty_factor = np.exp(-lambda_param * total_similarity)

            # 应用惩罚
            robust_shapley[m] = approx_shapley[m] * penalty_factor

        return robust_shapley
