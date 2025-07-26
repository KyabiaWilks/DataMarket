#import "./../template.typ": *

#show: project.with(
  theme: "project",
  course: "数据要素市场",
  title: "机器学习模型交易完整流程",
  author: "高文韬 钱满亮 王芷瑜",
  date: "2025-07-26",
  semester: "sp25"
)

= 1 #fakebold[问题描述]

#blockx[
  
]

= 2 #fakebold[文章的整体思路]

= 3 #fakebold[关键定理的描述]

= 4 #fakebold[实现的核心算法介绍]

== 4.1 #fakebold[基础复现]

=== 4.1.1 #fakebold[main.py]

总体目标：#fakebold[模拟一次完整的数据市场交易流程]，包括：
+ 市场定价(动态或UCB学习)
+ 买家诚实出价
+ 市场根据出价决定是否降噪并训练模型
+ 计算买家的收益(预测精度)
+ 市场向买家收取费用(基于Myerson公式)
+ 市场更新价格模型
+ 使用Shapley值分配卖家收入(带鲁棒性)
#figure[
#table(
  columns: 4,
  [步骤],
  [功能],
  [对应模块],
  [简要说明],
  [0.数据生成],
  [生成市场数据(特征 X 和标签 Y)],
  [`generate_data`(from `rmse`)],
  [创建模拟训练数据，用于收益计算和模型评估],
  [1.市场定价],
  [动态定价或UCB定价],
  [`choose_price()`(from `DynamicPricer`/`UCBPricer`)],
  [通过专家权重选择最优价格],
  [2&3.买家出价],
  [买家根据市场定价出价],
  [按照买家诚实出价的假设进行模拟设定，不涉及具体模块],
  [设定买家的估值和出价],
  [4&5.模型训练],
  [训练模型并计算预测增益],
  [`get_prediction_gain()`(from `HonestAuction`)],
  [使用降噪数据训练模型，计算预测精度],
  [6.收益计算],
  [计算买家收益和市场收入],
  [`calculate_revenue()`(from `HonestAuction`)],
  [基于Myerson支付规则计算买家应付费用],
  [7.价格更新],
  [更新市场定价模型],
  [`update_weights()`/`update_stats()`(from `DynamicPricer`/`UCBPricer`)],
  [使用刚获得的收入更新专家权重],
  [8.收入分配],
  [分配卖家收入(Shapley值)],
  [`shapley_robust()`(from `RevenueDivider`)],
  [使用鲁棒Shapley值方法对卖家贡献进行归因和分配收益]
)
  caption: main.py 各部分对应模块一览
]

=== 4.1.2 #fakebold[rmse.py]

负责为市场提供数据生成、模型训练和预测增益计算、收益计算与分配等功能。

==== 4.1.2.1. generate_data(M=10, T=100) 模拟数据生成器

输入参数：

  - M: 卖家数量（即特征维度数）

  - T: 时间步长或数据样本数量

#blockx[
  流程：

  + 生成特征矩阵 X ∈ ℝ^(M×T)，每一行是一个卖家的数据；

  + 生成一个长度为 M 的真实权重向量 true_weights；

  + 用线性组合 Y = true_weights · X + 噪声 生成目标变量；

  + 噪声项服从 𝒩(0, 0.5)，用于模拟预测误差。
]

输出：

  - X: 所有卖家的特征数据（二维数组）

  - Y: 合成后的目标变量（用于模拟训练/评价）

==== 4.1.2.2. ml_model = LinearRegression()

作用：

用来拟合从 X 到 Y 的预测模型，用于模拟市场在获取数据后能提升预测能力的场景。

#tip[该模型在其他文件中会用于计算“某个价格下，市场购买某些数据后的预测能力”，进而用于估算“收益”或“增益”。]

==== 4.1.2.3. gain_function_rmse(y_true, y_pred)
市场中用于衡量预测效果的 “数据增益函数”，用于反映模型训练后的效果是否更优。

#blockx[
  原理：

  计算 `RMSE(y_true, y_pred)`；

  归一化为 `Normalized RMSE = RMSE` / `std(y_true)`；

  增益函数定义为 `Gain = max(0, 1 - Normalized RMSE)`，取值 ∈ [0, 1]。
]

意义：
当模型预测效果越好，RMSE 越小，增益越大；
增益越高 → 数据越有价值 → 收益越大。

=== 4.1.3 #fakebold[HonestAuction.py]

实现了论文中的诚实拍卖机制，包括分配函数 (AF\*) 和收益函数 (RF\*)。

==== 4.1.3.1. 分配函数(\_allocation_function)

功能：根据买家的出价 b_n 与市场定价 p_n 的差值，决定是否对数据加入噪声，从而“降级”数据质量。

机制来源：论文 Example 4.1 的 AF\* 实现。

#blockx[
加噪逻辑：

- 如果 b_n >= p_n，买家可获得完整原始数据；

- 如果 b_n < p_n，对数据加上 ~𝒩(0, σ²) 噪声，其中：

```scss
σ ∝ (p_n - b_n) * noise_std
```
即出价越低，数据越差，这是激励买家诚实出价的关键机制。
]
==== 4.1.3.2. 预测增益函数(get_prediction_gain)
功能：训练模型并计算预测结果与真实结果之间的 预测增益 G。

#blockx[
流程：

用 `_allocation_function` 得降级版 X_tilde；

将 X_tilde.T 和 Y 喂给 `ml_model`(遵循 scikit-learn API，如 LinearRegression)；

用 `gain_function(y_true, y_pred)` 得增益指标(如 1 - RMSE)。
]

==== 4.1.3.3. 收益函数(calculate_revenue)

核心算法：Myerson 支付规则

$ r_n = b_n \u{00B7} G(b_n) - \u{222B}^(b_n)_0 G(z) d z $

含义：

- 第一项 $b_n \u{00B7} G(b_n)$：买家愿意为当前增益支付的金额；

- 第二项 $\u{222B}^(b_n)_0 G(z) d z$：信息租金，确保机制诚实激励；

两者相减就是市场应收费用。

数值实现方法：

#tip[
  这里一开始用的是 scipy.integrate.quad 进行区间积分，但老遇到达到最大次数限制后仍然无法收敛的问题。

  后来手动优化成使用 Simpson 积分法，数值稳定性更好,也没有再报错了。]

```python
z_vals = np.linspace(0, b_n, 100)
y_vals = [G(z) for z in z_vals]
integral = simpson(y_vals, z_vals)
```
=== 4.1.4 #fakebold[DynamicPricer.py]

该程序的目的是实现动态定价策略：

在数据市场中，根据拍卖反馈不断调整对价格的“信心”，从而自动寻找最优价格点。

==== 4.1.4.1 核心算法：MWU（Multiplicative Weights Update）：

算法步骤如下：

+ 将价格空间 [min_price, max_price] 离散为 num_experts 个价格（每个价格对应一个“专家”）；

+ 初始时，每个专家权重设为 1；

+ 在每一轮交易中：

  - 根据专家权重的归一化分布，随机抽取一个价格 p_n（相当于让一个专家出主意）；

  - 得到市场反馈（通过 auction_mechanism 得到的收益）；

  - 所有专家根据反馈更新权重（收益越好，权重涨得越多）；

#fakebold[更新公式：]

$ w_i^(n+1) \u{2261} w_i \u{00B7} (1+\u{03B4} \u{00B7} hat(g_i)) $

其中，$hat(g_i)$ 是专家 i 的归一化虚拟收益，$\u{03B4}$ 是学习率。

=== 4.1.5 #fakebold[RevenueDriver.py]

实现了一个 基于 Shapley 值的收益分配系统，用于衡量和分配多个“卖家”或“特征提供者”在一个预测模型中所做出的边际贡献。


== 4.2 #fakebold[进阶功能]

=== 4.2.1 #fakebold[UCBPricer.py]

=== 4.2.2 #fakebold[Security.py]

= 5 #fakebold[实验结果与分析]

== 5.1 #fakebold[基础复现]
== 5.1.1 #fakebold[实验结果]
#image("images/Dynamic.png")
== 5.1.2 #fakebold[实验分析]

按照图示步骤模拟了机器学习市场模型交易完整流程。

== 5.2 #fakebold[更多的定价算法]
== 5.2.1 #fakebold[实验结果]
#image("images/UCB.png")
== 5.2.2 #fakebold[实验分析]

== 5.3 #fakebold[隐私计算]
== 5.3.1 #fakebold[实验结果]
#image("images/ZKP.png")
#image("images/ZKP2.png")
== 5.3.2 #fakebold[实验分析]