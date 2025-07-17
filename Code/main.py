import numpy as np
from shared import ml_model, price_range
from RevenueDiver import RevenueDivider
from HonestAuction import HonestAuction
from DynamicPricer import DynamicPricer
from UCBPricer import UCBPricer
from Security.MarketVerificationService import MarketVerificationService
from Security.VerifiableSeller import VerifiableSeller
from rmse import gain_function_rmse, generate_data
from Security.SecurityMain import dataRegister
from sklearn.linear_model import LinearRegression

whichPricer = 1  # 可以选择 "DynamicPricer"(0) 或 "UCBPricer"(1)

# 0.数据注册阶段
print("--- 数据注册阶段 ---")

registered_features = dataRegister()
# 将所有已验证的特征组合成市场的数据集 X
X = np.array(registered_features)
print(f"--- 数据注册完成，市场中有 {X.shape} 个已验证的数据特征 ---\n")

# 1. 初始化市场组件
# 假设买家的估值和市场的价格都在  范围内
price_range = (50, 500)
if whichPricer == 0:
    pricer = DynamicPricer(price_range=price_range, num_experts=20, learning_rate_delta=0.1)
else:
    pricer = UCBPricer(price_range=price_range, num_experts=20, confidence_c=2.0)
auction = HonestAuction(ml_model=ml_model, gain_function=gain_function_rmse)
divider = RevenueDivider(ml_model=ml_model, gain_function=gain_function_rmse)

# 2. 生成数据
X, Y = generate_data(M=10, T=100)

# 3. 模拟单个买家 n 的交易
print("--- 开始模拟单次交易 ---")
print(f"使用的定价器: {'DynamicPricer' if whichPricer == 0 else 'UCBPricer'}")
# 步骤 1: 市场定价
p_n, chosen_index = pricer.choose_price()
print(f"步骤 1: 市场设定价格 p_n = {p_n:.2f}")

# 步骤 2 & 3: 买家到达并出价
# 假设一个买家，其真实估值为 200
mu_n = 200.0
# 根据真实性原则，买家诚实出价
b_n = mu_n
b_n = float(b_n)  # 明确转成 float

print(f"步骤 2 & 3: 买家到达，真实估值 μ_n = {mu_n:.2f}，诚实出价 b_n = {b_n:.2f}")

# 步骤 4 & 5: 市场分配数据，买家获得增益
print("步骤 4 & 5: 市场分配数据并计算预测增益...")
# 为了演示，我们先计算一下无噪声时的基准增益
gain_no_noise = auction.get_prediction_gain(X, Y, p_n=b_n, b_n=b_n) # b_n >= p_n, 无噪声
# 计算实际出价下的增益
gain_actual = auction.get_prediction_gain(X, Y, p_n, b_n)
print(f"  - 基准增益 (无噪声): {gain_no_noise:.4f}")
print(f"  - 实际增益 (根据出价): {gain_actual:.4f}")

# 步骤 6: 市场收取收益
revenue_n = auction.calculate_revenue(X, Y, p_n, b_n)
print(f"步骤 6: 市场向买家收取收益 r_n = {revenue_n:.2f}")

# 步骤 7: 市场更新价格模型
if whichPricer == 0:
    pricer.update_weights(auction, X, Y, b_n)
else:
    revenue_n = auction.calculate_revenue(X, Y, p_n, b_n)
    pricer.update_stats(chosen_index, revenue_n)
print(f"步骤 7: 市场价格模型权重已更新。")

# 步骤 8: 市场分配收益给卖家
print("步骤 8: 市场计算并分配收益给卖家...")
# 使用鲁棒的Shapley值分配，设置K=50次采样
shapley_values = divider.shapley_robust(X, Y, K=50)

# 归一化Shapley值作为分配比例
if np.sum(shapley_values) > 0:
    allocation_ratios = shapley_values / np.sum(shapley_values)
else:
    allocation_ratios = np.ones(X.shape) / X.shape # 均分

seller_revenues = revenue_n * allocation_ratios
print(f"  - 计算出的Shapley值 (归一化前): {np.round(shapley_values, 4)}")
print(f"  - 各卖家的收益分配: {np.round(seller_revenues, 2)}")

print("--- 模拟结束 ---")