// server.js（ES Module版本）
import express from 'express';
import cors from 'cors';
import jwt from 'jsonwebtoken';
import cookieParser from 'cookie-parser';
import bodyParser from 'body-parser';

const app = express();
const PORT = 3001;
const JWT_SECRET = 'your-super-secret-key'; // 在生产环境中应使用环境变量

app.use(cors({ origin: 'http://localhost:5173', credentials: true }));
app.use(bodyParser.json());
app.use(cookieParser());

// 模拟用户数据库
const users = [{ username: 'testuser', password: 'password123' }];

// 登录接口
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        const token = jwt.sign({ username: user.username }, JWT_SECRET, { expiresIn: '1h' });
        res.cookie('token', token, { httpOnly: true, secure: false, sameSite: 'lax' }); // 在生产中应设 secure: true
        res.json({ message: '登录成功', user: { username: user.username } });
    } else {
        res.status(401).json({ message: '用户名或密码错误' });
    }
});

// 验证用户状态接口
app.get('/api/profile', (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(401).json({ message: '未授权' });
    }
    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        res.json({ user: { username: decoded.username } });
    } catch (error) {
        res.status(401).json({ message: 'Token 无效' });
    }
});

// 登出接口
app.post('/api/logout', (req, res) => {
    res.clearCookie('token');
    res.json({ message: '登出成功' });
});

// 模拟拍卖流程接口
app.post('/api/run-auction', (req, res) => {
    const { modelId, bid, taskData } = req.body;
    console.log(`收到拍卖请求: 模型ID=${modelId}, 出价=${bid}`);

    // 模拟后端处理延迟
    setTimeout(() => {
        // 模拟论文复现程序的输出
        const result = {
            market_price_offered: (Math.random() * 200 + 150).toFixed(2), // 市场定价 p_n
            your_bid: bid,
            prediction_gain_achieved: (0.85 + Math.random() * 0.1).toFixed(4), // 预测增益 G
            cost_to_you: (bid * 0.5 + Math.random() * 10).toFixed(2), // 最终费用 r_n
            seller_payouts: [], // 示例：空数组或你可以填充模拟数据
        };
        res.json(result);
    }, 2000);
});

app.listen(PORT, () => {
    console.log(`模拟后端服务器运行在 http://localhost:${PORT}`);
});