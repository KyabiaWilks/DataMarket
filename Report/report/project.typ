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
  columns: 3,
  [步骤],
  [对应模块],
  [简要说明],
  [0.生成市场数据(特征 X 和标签 Y)],
  [`generate_data`(from `rmse`)],
  [创建模拟训练数据，用于收益计算和模型评估],
  [1.动态定价或UCB定价],
  [`choose_price()`(from `DynamicPricer`/`UCBPricer`)],
  [通过专家权重选最优价格],
  [2&3.买家出价],
  [按买家诚实出价的假设进行模拟，不涉及具体模块],
  [设定买家的估值和出价],
  [4&5.训练模型并计算预测增益],
  [`get_prediction_gain()`(from `HonestAuction`)],
  [使用降噪数据训练模型，计算预测精度],
  [6.计算买家收益和市场收入],
  [`calculate_revenue()`(from `HonestAuction`)],
  [基于Myerson支付规则计算买家应付费用],
  [7.更新市场定价模型],
  [`update_weights()`/`update_stats()`(from `DynamicPricer`/`UCBPricer`)],
  [使用刚获得的收入更新专家权重],
  [8.分配卖家收入(Shapley值)],
  [`shapley_robust()`(from `RevenueDivider`)],
  [使用鲁棒Shapley值方法对卖家贡献进行归因和分配收益]
)
  caption: main.py 各部分对应模块一览
]

=== 4.1.2 #fakebold[数据准备与模型准备：rmse.py]

负责为市场提供数据生成、模型训练和预测增益计算、收益计算与分配等功能。

==== 4.1.2.1. generate_data(M=10, T=100) 模拟数据生成器

功能说明：

模拟多个数据卖家提供特征数据，目标值由这些特征加权（线性模型）生成并加入噪声。

#blockx[
  核心算法：
  ```perl
  for each seller i in M:
      generate feature vector X[i] of length T
  generate true weights w_true of length M
  Y = dot(w_true, X) + gaussian_noise
  return X, Y
  ```
]

==== 4.1.2.2. ml_model = LinearRegression()

功能说明：

使用线性回归模型来学习卖家提供数据与目标值 Y 的关系。

#blockx[
  核心算法：
  ```perl
  initialize ml_model as LinearRegression
  ```
]

==== 4.1.2.3. gain_function_rmse(y_true, y_pred)
功能说明：

评估模型预测质量，返回一个增益值（越接近 1 表示模型越好）。

#blockx[
  核心算法：
  ```perl
  rmse = sqrt(mean_squared_error(y_true, y_pred))
  y_std = std(y_true)
  if y_std == 0:
      return 1.0
  normalized_rmse = rmse / y_std
  gain = max(0, 1 - normalized_rmse)
  return gain
  ```
]

=== 4.1.3 #fakebold[诚实的机器学习模型拍卖：HonestAuction.py]

实现了论文中的诚实拍卖机制，包括分配函数 (AF\*) 和收益函数 (RF\*)。

==== 4.1.3.1. 分配函数(\_allocation_function)

功能说明：根据买家的出价 b_n 与市场定价 p_n 的差值，决定是否对数据加入噪声，从而“降级”数据质量。

机制来源：论文 Example 4.1 的 AF\* 实现。

#blockx[
  核心算法：
  ```perl
  if bid >= price: return X else: return X + noise(price - bid)
  ```
]

==== 4.1.3.2. 预测增益函数(get_prediction_gain)

功能说明：训练模型并计算预测结果与真实结果之间的 预测增益 G。

#blockx[
核心算法：
  ```perl
  X_tilde = AF*(X, p, b) → model.fit → gain = G(y_true, y_pred)
  ```
]
==== 4.1.3.3. 收益函数(calculate_revenue)

功能说明：按 Myerson 支付规则，积分求信息租金，再计算收益

#blockx[核心算法：Myerson 支付规则

$ r_n = b_n \u{00B7} G(b_n) - \u{222B}^(b_n)_0 G(z) d z $

含义：

- 第一项 $b_n \u{00B7} G(b_n)$：买家愿意为当前增益支付的金额；

- 第二项 $\u{222B}^(b_n)_0 G(z) d z$：信息租金，确保机制诚实激励；

两者相减就是市场应收费用。]

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

==== 4.1.4.1 核心算法：MWU(Multiplicative Weights Update)：

算法步骤如下：

+ 将价格空间 [min_price, max_price] 离散为 num_experts 个价格(每个价格对应一个“专家”)；

+ 初始时，每个专家权重设为 1；

+ 在每一轮交易中：

  - 根据专家权重的归一化分布，随机抽取一个价格 p_n(相当于让一个专家出主意)；

  - 得到市场反馈(通过 auction_mechanism 得到的收益)；

  - 所有专家根据反馈更新权重(收益越好，权重涨得越多)；

#fakebold[更新公式：]

$ w_i^(n+1) \u{2261} w_i \u{00B7} (1+\u{03B4} \u{00B7} hat(g_i)) $

其中，$hat(g_i)$ 是专家 i 的归一化虚拟收益，$\u{03B4}$ 是学习率。

=== 4.1.5 #fakebold[RevenueDriver.py]

实现了一个 基于 Shapley 值的收益分配系统，用于衡量和分配多个“卖家”或“特征提供者”在一个预测模型中所做出的边际贡献。

==== 4.1.5.1. `shapley_approx` — 近似 Shapley 值

功能说明：

使用 K 次随机排列，近似计算每个卖家对预测任务的 Shapley 边际贡献。

#blockx[
核心算法
```perl
函数 shapley_approx(X, Y, K):
    初始化每个卖家的 shapley 值为 0
    对于 k in 1 到 K:
        生成一个随机排列 perm
        初始化 gain_predecessors = 0
        对于 perm 中的每个卖家 i:
            gain_current = get_gain_for_subset(前 i 个 + 当前卖家)
            marginal = gain_current - gain_predecessors
            将 marginal 加入当前卖家的 shapley 值
            gain_predecessors = gain_current
    返回 shapley 值的平均
```
]
==== 4.1.5.2. `shapley_robust` — 鲁棒 Shapley 值

功能说明：

使用 K 次随机排列，近似计算每个卖家对预测任务的 Shapley 边际贡献。

#blockx[
核心算法
```perl
函数 shapley_robust(X, Y, K, λ):
    approx_shapley = shapley_approx(X, Y, K)
    计算 X 中每个卖家特征的 cosine 相似度矩阵 S
    对于每个卖家 i:
        total_sim = sum(S[i]) - 1
        penalty = exp(-λ * total_sim)
        robust_shapley[i] = approx_shapley[i] * penalty
    返回 robust_shapley
```
]
 
== 4.2 #fakebold[进阶功能]

=== 4.2.1 #fakebold[UCBPricer.py]

实现了更多样的定价机制： UCB(Upper Confidence Bound)定价策略。

==== 4.2.1.1.核心算法
#figure[
  #image("images/UCB_theory.png")
  caption: UCB 定价策略的代码参考了这个课内slide
  ]

`choose_price`: 基于UCB算法选择一个当前最优价格

#blockx[
  UCB 核心算法：
  ```python
  average_reward + sqrt((c * log(total_rounds)) / count)
  ```
]

`update_stats`：某轮价格尝试后，用实际收益 reward 更新该价格（专家）的平均收益。

#blockx[
  核心算法：
  ```python
  counts[i] += 1
  values[i] = ((counts[i] - 1)/counts[i]) * old_value + (1/counts[i]) * reward
  ```
]
==== 4.2.1.2.对比UCB定价 与 Dynamic定价(基于ML回归预测) 
#table(
  columns: 3,
  [对比维度],
  [UCB 定价机制],
  [Dynamic 定价机制(ML 回归)],
  [核心原理],
  [多臂老虎机 + 置信上界],
  [机器学习模型预测最优价格/收益],
  [是否依赖标签],
  [不依赖精确标签，基于经验更新收益估计],
  [需要监督数据(历史价格 → 收益)],
  [探索能力],
  [强(自动探索未尝试价格)],
  [弱(依赖已有训练数据)],
  [适用场景],
  [- 在线广告投放价格
- 即时拍卖价格选择],
  [- 产品销售预测定价
- 卖家特征驱动的市场机制
],
  [响应速度],
  [初期慢，长期收敛],
  [初期快，易过拟合或失效于新环境]
)

=== 4.2.2 #fakebold[Security.py]

==== 4.2.2.1. 总流程
#figure[
  #image("images/flowchart.png")
  caption: 安全模式+main综合后 的工作流程，出于工作量考虑只做了一种定价策略的实现
]
#table(
  columns:3,

  [步骤],
  [对应模块],
  [功能简述],
  [1.初始化市场],
  [`Marketplace` (market_mechanisms.py)],
  [提供市场整体逻辑，包括注册验证服务、VC验证等],
  [2&3.创建卖家对象],
  [`VerifiableSeller` (market_participants.py)  `VerifiableSeller. set_data()`],
  [卖家类，具备：生成数据、提交注册数据包(含签名+ZKP)的能力,设置好数据],
  [4.生成注册包并提交],
  [`VerifiableSeller. get_data_ registration_package()`],
  [提供数据包(含数据、签名、ZKP)提交市场],
  [5.数据注册并验证],
  [`Marketplace. verification_service. register_data()`],
  [使用伪造检测+重复检测机制，确保数据来源独立真实],
  [6\~8.创建定价器、竞拍器、收入分配器],
  [同4.1],
  [同4.1],
  [9.创建买家对象],
  [`BuyerWithCredentials` (market_participants.py)],
  [买家类，支持 VC 认证管理和出价行为],
  [10.添加买家 VC],
  [`BuyerWithCredentials. add_credential()`],
  [添加买家凭证(如医疗研究员资格)],
  [11.验证买家资格],
  [`Marketplace. verify_buyer_credentials()`],
  [检查某买家是否持有合法 VC],
  [12\~23.正常进行后续拍卖流程],
  [同4.1],
  [同4.1]
)

==== 4.2.2.2.ZKP验证卖家数据所有权

主要功能：
`MarketVerificationService`	验证并注册卖家的数据包，防止数据抄袭，使用零知识证明（ZKP）确认所有权

#blockx[
  核心算法：
  ZKP验证 `MarketVerificationService.register_data()`
  
  ```
  If data_hash in registered_data:
    Reject
  If not verify_zkp(public_key, data_hash, zkp):
      Reject
  Add data_hash to registered_data
  Accept
  ```

  流程：
  - hashlib.sha256(...)	计算数据的不可逆摘要，作为数据唯一表示
  - sign(...)	使用私钥对哈希签名（如使用ECDSA），表明“我拥有此数据”
  - generate_zkp_of_signature(...)	构造一个零知识证明，证明签名是由拥有该公钥对应私钥者生成的，而不暴露私钥
]
==== 4.2.2.3. VC验证买家身份

主要功能：
- `BuyerWithCredentials.wallet`买家存储从平台获取的访问凭证 VC
- `BuyerWithCredentials.present_credential()`向市场出示某一类凭证，供验证逻辑使用


#blockx[
核心算法：
- `wallet`：一个字典，存储类型化的凭证（如 "Access", "Reputation", "Score"）

- `add_credential(...)`：添加凭证，例如来自市场管理员

- `present_credential(...)`：买家在交易时出示凭证
]

#tip[
  这段和论文的关系就比较小了，但是鉴于信安专业+课上还是提过一些隐私计算所以想到这个方向后还是毅然决然地做了。

  这里本来想写得深入一点，还为此研究了一下Zokrates，但在编译zok文件的时候失败了，调了一天也没调出来，现在的版本大部分是引用各种库，其中一部分可以说引得我自己也不太了解，只能说更重要的是引入隐私计算这个步骤本身吧。]

= 5 #fakebold[实验结果与分析]

== 5.1 #fakebold[基础复现]
== 5.1.1 #fakebold[实验结果]
#image("images/Dynamic.png")
== 5.1.2 #fakebold[实验分析]

按照图示步骤模拟了机器学习市场模型交易完整流程。

其中，诚实的机器学习模型拍卖（Honest Auction），MWU 算法动态定价（Multiplicative Weights Update） 和 收益分配（Shapley值） 均在流程中有实现，已在上一节中分别给出核心算法；对于用户数据的模拟则有所简化。

== 5.2 #fakebold[更多的定价算法]
== 5.2.1 #fakebold[实验结果]
#image("images/UCB.png")
== 5.2.2 #fakebold[实验分析]
按照图示步骤模拟了机器学习市场模型交易完整流程。

将定价算法从DynamicPricer改为UCBPricer，使用UCB定价策略替代了MWU定价策略。在数据生成和定价环节均有变化，可以看到程序成功跑通。

== 5.3 #fakebold[隐私计算]
== 5.3.1 #fakebold[实验结果]
#image("images/ZKP.png")
#image("images/ZKP2.png")
== 5.3.2 #fakebold[实验分析]
按照图示步骤模拟了带上隐私计算功能的机器学习市场模型交易完整流程。

其中，生成公钥和ZKP的过程均在输出中有体现，对于VC过程，Alice的数据模拟了VC通过并正常进行拍卖定价和收益分配的全流程，而Bob的数据则模拟了VC验证失败的情况，可以看到拍卖正常中止。