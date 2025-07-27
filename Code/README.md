## 核心代码文件简介

- `main.py`：主程序入口，整合了数据市场的各个部分。
- `rmse.py`：负责为市场提供数据生成、模型训练和预测增益计算、收益计算与分配等功能。
- `DynamicPricer.py`：实现动态定价策略：在数据市场中，根据拍卖反馈不断调整对价格的“信心”，从而自动寻找最优价格点。
- `HonestAuction.py`：实现了一个诚实拍卖机制，允许卖家在拍卖中报告他们的真实价值。
- `shared.py`：包含共享机器学习模型的实现，提供了一个线性回归模型的示例。
- `RevenueDriver.py`：实现了一个 基于 Shapley 值的收益分配系统，用于衡量和分配多个“卖家”或“特征提供者”在一个预测模型中所做出的边际贡献。
- `UCBPricer.py`：实现了一个基于上置信界（UCB）的定价策略，旨在通过探索和利用的平衡来最大化收益。
- `Security/smain.py`：实现了隐私计算部分，使用安全多方计算（SMC）技术来保护数据隐私。

## 运行代码

### 核心算法

- 配置环境：
## 核心代码文件简介

- `main.py`：主程序入口，整合了数据市场的各个部分。
- `rmse.py`：负责为市场提供数据生成、模型训练和预测增益计算、收益计算与分配等功能。
- `DynamicPricer.py`：实现动态定价策略：在数据市场中，根据拍卖反馈不断调整对价格的“信心”，从而自动寻找最优价格点。
- `HonestAuction.py`：实现了一个诚实拍卖机制，允许卖家在拍卖中报告他们的真实价值。
- `shared.py`：包含共享机器学习模型的实现，提供了一个线性回归模型的示例。
- `RevenueDriver.py`：实现了一个 基于 Shapley 值的收益分配系统，用于衡量和分配多个“卖家”或“特征提供者”在一个预测模型中所做出的边际贡献。
- `UCBPricer.py`：实现了一个基于上置信界（UCB）的定价策略，旨在通过探索和利用的平衡来最大化收益。
- `Security/smain.py`：实现了隐私计算部分，使用安全多方计算（SMC）技术来保护数据隐私。

## 运行代码

### 核心算法

- 配置环境：

```bash
```bash
pip install -r requirements.txt
python main.py
```
```

### 隐私计算
### 隐私计算

```bash
cd Security
python smain.py

### 前端

```bash
cd ml-model-market
npm install react-router-dom axios react-icons jwt-decode
npm install @chakra-ui/react@2.8.2 @emotion/react@11 @emotion/styled@11 framer-motion@6
npm install express cors jsonwebtoken cookie-parser body-parser multer

cd server
node server.js

cd ..
npm run dev
```