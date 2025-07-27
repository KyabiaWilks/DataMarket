import numpy as np
from scipy.integrate import quad
from scipy.integrate import simpson
from shared import ml_model, price_range

class HonestAuction:
    """
    实现了论文中的诚实拍卖机制，包括分配函数 (AF*) 和收益函数 (RF*)。
    """
    def __init__(self, ml_model, gain_function):
        """
        初始化拍卖机制。

        Args:
            ml_model: 一个遵循 scikit-learn API 的机器学习模型实例 (有.fit 和.predict 方法)。
            gain_function: 一个函数，输入 (y_true, y_pred)，输出预测增益 G。
        """
        self.ml_model = ml_model
        self.gain_function = gain_function

    def _allocation_function(self, X, p_n, b_n, noise_std=0.1):
        """
        分配函数 AF* (Allocation Function)。
        根据价格 p_n 和出价 float(b_n) 的差异，向数据 X 添加高斯噪声来降级其质量。
        这是论文中 Example 4.1 的实现。

        Args:
            X (np.array): 原始特征数据 (M, T)。
            p_n (float): 市场设定的价格。
            float(b_n) (float): 买家的出价。
            noise_std (float): 基础噪声的标准差。

        Returns:
            np.array: 降级后的数据 X_tilde。
        """
        if float(b_n) >= p_n:
            return X
        else:
            # 噪声大小与价格和出价的差值成正比
            noise_magnitude = max(0, p_n - float(b_n))
            noise = np.random.normal(0, noise_std * noise_magnitude, X.shape)
            X_tilde = X + noise
            return X_tilde

    def get_prediction_gain(self, X, Y, p_n, b_n):
        """
        在给定价格和出价下，计算预测增益 G。

        Args:
            X (np.array): 原始特征数据 (M, T)。
            Y (np.array): 目标预测任务数据 (T,)。
            p_n (float): 市场价格。
            float(b_n) (float): 买家出价。

        Returns:
            float: 预测增益 G。
        """
        # 1. 根据价格和出价分配（可能降级的）数据
        X_tilde = self._allocation_function(X, p_n, float(b_n))
        
        # 2. 训练模型并进行预测
        # 注意：在实际应用中，需要划分训练集和测试集。为简化，这里在整个数据集上操作。
        # scikit-learn 的线性回归需要 (n_samples, n_features) 格式
        # 我们将 T 视为样本数，M 视为特征数
        X_train = X_tilde.T  # Shape: (T, M)
        y_train = Y          # Shape: (T,)
        
        self.ml_model.fit(X_train, y_train)
        y_pred = self.ml_model.predict(X_train)
        
        # 3. 计算预测增益
        gain = self.gain_function(y_train, y_pred)
        return gain

    # def calculate_revenue(self, X, Y, p_n, b_n):
    #     """
    #     收益函数 RF* (Revenue Function)。
    #     根据 Myerson 支付规则计算应向买家收取的费用。

    #     Args:
    #         X (np.array): 原始特征数据。
    #         Y (np.array): 目标预测任务数据。
    #         p_n (float): 市场价格。
    #         float(b_n) (float): 买家出价。

    #     Returns:
    #         float: 应收取的收益 r_n。
    #     """
    #     # 计算在出价 float(b_n) 下的实际增益
    #     gain_at_b_n = self.get_prediction_gain(X, Y, p_n, float(b_n))
        
    #     # 定义需要积分的函数 g(z) = G(Y, M(AF*(z, p_n)))
    #     def gain_as_function_of_bid(z):
    #         return self.get_prediction_gain(X, Y, p_n, z)
            
    #     # 使用数值积分计算信息租金
    #     # quad 返回一个元组 (积分结果, 估计误差)
    #     integral_part, _ = quad(gain_as_function_of_bid, 0, float(b_n), limit=100)
        
    #     # Myerson 支付规则
    #     revenue = float(b_n) * gain_at_b_n - integral_part
        
    #     return float(max(0, revenue)) # 确保收益不为负
    
    # 工作量：优化积分
    def calculate_revenue(self, X, Y, p_n, b_n):
        gain_at_b_n = self.get_prediction_gain(X, Y, p_n, float(b_n))
        
        # 定义需要积分的函数 g(z) = G(Y, M(AF*(z, p_n)))
        def gain_as_function_of_bid(z):
            return self.get_prediction_gain(X, Y, p_n, z)
        
        # 将积分区间分成两部分进行积分
        b_n_half = float(b_n) / 2
        integral_part_1, _ = quad(gain_as_function_of_bid, 0, b_n_half, limit=50)
        integral_part_2, _ = quad(gain_as_function_of_bid, b_n_half, float(b_n), limit=50)
        
        # 合并积分结果
        integral_part = integral_part_1 + integral_part_2
        
        # Myerson 支付规则
        revenue = float(b_n) * gain_at_b_n - integral_part
        
        return float(max(0, revenue))  # 确保收益不为负

    def calculate_revenue(self, X, Y, p_n, b_n):
        gain_at_b_n = self.get_prediction_gain(X, Y, p_n, float(b_n))
        
        # 定义需要积分的函数
        def gain_as_function_of_bid(z):
            return self.get_prediction_gain(X, Y, p_n, z)
        
        # 使用 Simpson 积分
        z_vals = np.linspace(0, float(b_n), 100)  # 划分为 100 个点
        y_vals = np.array([gain_as_function_of_bid(z) for z in z_vals])
        integral_part = simpson(y_vals, z_vals)
        
        # 计算收益
        revenue = float(b_n) * gain_at_b_n - integral_part
        
        return float(max(0, revenue))

