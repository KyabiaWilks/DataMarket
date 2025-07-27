import numpy as np
from shared import ml_model, price_range
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# 模拟数据生成
def generate_data(M=10, T=100):
    # M 个卖家，每个提供长度为 T 的特征向量
    X = np.random.rand(M, T) * 10
    # 真实权重
    true_weights = np.random.randn(M)
    # Y 是 X 的带噪声线性组合
    Y = np.dot(true_weights, X) + np.random.normal(0, 0.5, T)
    return X, Y


# 机器学习模型
ml_model = LinearRegression()


# 增益函数 G = 1 - Normalized RMSE
def gain_function_rmse(y_true, y_pred):
    """
    计算 1 - Normalized RMSE 作为增益函数
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    # 归一化RMSE，使其值在 [0, inf) 之间，通常接近
    # 通过除以目标变量的标准差进行归一化
    y_std = np.std(y_true)
    if y_std == 0:
        return 1.0  # 避免除以零
    normalized_rmse = rmse / y_std
    # 增益为 1 - nrmse，确保值越大越好，并限制在 <= 1
    return max(0, 1 - normalized_rmse)
