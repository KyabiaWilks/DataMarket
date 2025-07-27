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

pip install -r requirements.txt
python main.py
```

### 隐私计算

环境版本推荐：python3.10
这里我一开始用的是3.13，似乎会报错。

```bash
pip install cffi petlib bplib
```

特别地，安装 bplib 时可能会遇到一些问题，以下是我的解决方法：
```bash
wget https://pypi.tuna.tsinghua.edu.cn/packages/20/f2/9687045ddc885ee3a14075a1b7f2a8220fa922a80ae3ad567983f179b016/bplib-0.0.6.tar.gz#sha256=040deb52c4c5b194dcdba4c94150b9976622ca68e1d1296f17237e9d37071936
tar -xvzf bplib-0.0.6.tar.gz
```
进入文件 bplib/src/bp_fp2.c 
修改这行：
```c
if (!BN_zero(a->f[0]) || !BN_zero(a->f[1]))
    return 1;
```
改为：
```c
BN_zero(a->f[0]);
BN_zero(a->f[1]);
```
保存并退出后再运行：
```bash
sudo apt install build-essential libssl-dev libgmp-dev python3-dev
pip install cffi pycparser petlib==0.0.45 --no-build-isolation -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install . --no-build-isolation -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install zksk -i https://pypi.tuna.tsinghua.edu.cn/simple
```
即可成功配置环境。

```bash
cd Security
python smain.py

```

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