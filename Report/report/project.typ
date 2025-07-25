#import "../template.typ": *

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

总体目标：模拟一次完整的数据市场交易流程，包括：

+ 市场定价（动态学习）
+ 买家诚实出价
+ 市场根据出价决定是否降噪并训练模型
+ 计算买家的收益（预测精度）
+ 市场向买家收取费用（基于Myerson公式）
+ 市场更新价格模型
+ 使用Shapley值分配卖家收入（带鲁棒性）

=== 4.1.2 #fakebold[HonestAuction.py]
=== 4.1.3 #fakebold[DynamicPricer.py]
=== 4.1.4 #fakebold[rmse.py]
=== 4.1.5 #fakebold[RevenueDriver.py]

== 4.2 #fakebold[进阶功能]

=== 4.2.1 #fakebold[UCBPricer.py]
=== 4.2.2 #fakebold[Security.py]

= 5 #fakebold[实验结果与分析]

== 5.1 #fakebold[基础复现]
== 5.1.1 #fakebold[实验结果]
#image("images/Dynamic.png")
== 5.1.2 #fakebold[实验分析]

== 5.2 #fakebold[更多的定价算法]
== 5.2.1 #fakebold[实验结果]
#image("images/UCB.png")
== 5.2.2 #fakebold[实验分析]

== 5.3 #fakebold[隐私计算]
== 5.3.1 #fakebold[实验结果]
#image("images/ZKP.png")
== 5.3.2 #fakebold[实验分析]