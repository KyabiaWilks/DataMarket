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

随着机器学习技术的快速发展，数据已成为推动AI模型性能提升的核心要素。然而，如何在保证公平性和激励相容性的前提下，构建一个有效的数据交易市场仍然是一个重要挑战。本文研究的核心问题是设计一个#fakebold[双边数据市场]（two-sided data market），其中：

- #fakebold[数据卖家]：拥有各种特征数据的提供者，希望通过出售数据获得收益
- #fakebold[数据买家]：需要数据来训练机器学习模型以提升预测精度的用户

该市场面临的主要挑战包括：

1. #fakebold[定价机制设计]：如何为不同质量和价值的数据制定合理价格
2. #fakebold[激励相容性]：如何确保买家诚实报告其对数据的真实估值
3. #fakebold[公平收益分配]：如何根据不同卖家数据的边际贡献公平分配收益
4. #fakebold[数据质量控制]：如何防止数据复制和低质量数据的恶意投放

本文提出了一个完整的市场框架，通过结合拍卖理论、博弈论和Shapley值理论，解决了上述关键问题。

= 2 #fakebold[文章的整体思路]

文章采用了一个#fakebold[三步骤的系统性方法]来构建数据市场：

== 2.1 #fakebold[第一步：诚实机器学习模型拍卖机制]

基于#fakebold[Myerson拍卖理论]设计了一个激励相容的拍卖机制：

- #fakebold[分配函数 AF\*]：根据买家出价决定数据质量。如果出价低于市场定价，则对数据添加噪声进行"降级"
- #fakebold[支付函数 RF\*]：采用Myerson支付规则 $r_n = b_n dot G(b_n) - integral_0^(b_n) G(z) dif z$，确保买家诚实出价是占优策略

该机制的核心思想是通过#fakebold[数据质量分级]来实现价格歧视，激励买家诚实报告估值。

== 2.2 #fakebold[第二步：动态定价算法]

由于市场环境的不确定性，采用了两种在线学习算法进行动态定价：

- #fakebold[MWU算法]（Multiplicative Weights Update）：将价格空间离散化为多个"专家"，通过专家权重更新机制学习最优定价策略
- #fakebold[UCB算法]（Upper Confidence Bound）：基于置信区间的探索-利用策略，平衡价格探索与收益最大化

这些算法能够在#fakebold[零后悔]（zero regret）的理论保证下，逐步收敛到最优价格。

== 2.3 #fakebold[第三步：基于Shapley值的收益分配]

为了公平分配卖家收益，文章提出了#fakebold[鲁棒Shapley值]方法：

- #fakebold[标准Shapley值]：衡量每个卖家数据对模型预测精度的边际贡献
- #fakebold[鲁棒性改进]：通过相似性度量和指数加权，防止数据复制攻击，确保分配的公平性

该方法解决了传统Shapley值计算复杂度高和容易被操纵的问题。

= 3 #fakebold[关键定理的描述]

== 3.1 #fakebold[定理5.1：真实性保证]

#fakebold[定理陈述]：对于分配函数 AF*，当且仅当假设1成立时，性质3.1（真实性）可以实现，此时 RF* 保证真实性。

#fakebold[证明思路]：
这是Myerson支付函数的经典结果。证明分为两个方向：

1. #fakebold[正向]：假设买家真实出价 $b_n = \mu_n$，通过单调性条件证明偏离策略不会带来更高收益
2. #fakebold[反向]：如果机制是真实的，则增加的分配不能降低准确性

关键在于买家效用函数的设计，即买家的效用仅来自于获得的估计质量 $Y_n$，而非特定的数据集分配。

== 3.2 #fakebold[定理5.2：收益最大化]

#fakebold[定理陈述]：设假设1、3、4成立，设 $p_(n,n in [N])$ 为算法1的输出。通过选择算法超参数 $epsilon = (L sqrt(N))^(-1)$，$delta = sqrt(log(abs(cal(B)_(upright("net"))(epsilon)))/N)$，总平均后悔有界为：

$frac(1, N) bb(E)[cal(R)(N)] lt.eq C cal(B)_(upright("max")) sqrt(frac(log(cal(B)_(upright("max")) L sqrt(N)), N)) = O(sqrt(frac(log(N), N)))$

#fakebold[证明思路]：
1. 首先证明固定价格的后悔界限
2. 利用MWU算法的归纳关系式，建立权重更新的递推关系
3. 通过对数不等式和泰勒展开，得到期望收益的渐近界限

该定理说明算法1是零后悔算法，收益界限与特征数量M无关。

== 3.3 #fakebold[定理5.3：收益分配中的公平性]

#fakebold[定理陈述]：设 $psi_(n,"shapley")$ 为满足性质3.3（Shapley公平性）的唯一向量。对于算法2，选择超参数 $K > (M log(2 slash delta)) slash (2 epsilon^2)$，其中 $delta, epsilon > 0$，则以概率 $1 - delta$，算法2的输出 $hat(psi)_n$ 满足：

$||psi_(n,"shapley") - hat(psi)_n||_("infinity") < epsilon$


#fakebold[证明思路]：
这是对Shapley值的 $epsilon$-近似。证明基于：
1. 将Shapley值表示为期望形式
2. 利用有界支撑和独立性，应用Hoeffding不等式
3. 通过联合界限控制所有坐标的误差

该定理给出了计算Shapley值的有限样本保证，使得实际应用中可以通过有限采样获得理论保证的近似解。

== 3.4 #fakebold[定理5.4：抗复制鲁棒性]

#fakebold[定理陈述]：设假设2成立。对于算法3，选择超参数 $K >= (M log(2 slash delta)) slash (2(epsilon slash 3)^2)$，$lambda = log(2)$，其中 $delta, epsilon > 0$，则以概率 $1 - delta$，算法3的输出 $psi_n$ 是"$epsilon$-抗复制鲁棒"的，即满足性质3.4（抗复制鲁棒性）。

#fakebold[证明思路]：
1. 构造包含复制特征的增广集合 $S^+$
2. 证明指数惩罚函数 $exp(-lambda sum_(j in [M] \\ {m}) cal("SM")(X_m, X_j))$ 的鲁棒性条件
3. 利用相似性度量的性质，证明复制特征会被指数加权显著降权

该定理确保了即使存在数据复制攻击，收益分配仍然保持公平性。

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