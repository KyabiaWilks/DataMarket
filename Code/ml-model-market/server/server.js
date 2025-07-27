// server.js（ES Module版本）
import express from 'express';
import cors from 'cors';
import jwt from 'jsonwebtoken';
import cookieParser from 'cookie-parser';
import bodyParser from 'body-parser';
import { execFile } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import multer from 'multer';

// 当前模块的 __dirname 模拟
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3001;
const JWT_SECRET = 'your-super-secret-key'; // 在生产环境中应使用环境变量

app.use(cors({ origin: 'http://localhost:5173', credentials: true }));
app.use(bodyParser.json());
app.use(cookieParser());

// 模拟用户数据库
const users = [{ username: 'testuser', password: 'password123' }];
// 设置上传目录
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, 'uploads'));  // 确保 uploads 目录存在
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname); // 避免重名
  }
});

const upload = multer({ storage });

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

app.post('/api/run-auction', (req, res) => {
    const { modelId, bid, taskData } = req.body;
    const script = path.join(__dirname, 'run_auction.py');

    execFile('python3', [script, bid, modelId, JSON.stringify(taskData)], (error, stdout, stderr) => {
        if (error) {
            console.error('运行 Python 出错:', error);
            res.status(500).json({ error: '执行失败' });
            return;
        }
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (e) {
            res.status(500).json({ error: '解析 Python 输出失败', raw: stdout });
        }
    });
});


app.listen(PORT, () => {
    console.log(`模拟后端服务器运行在 http://localhost:${PORT}`);
});

app.post('/api/verify-model', upload.single('file'), (req, res) => {
  const { modelId } = req.body;
  const filePath = req.file.path;

  execFile('python3', [
    path.join(__dirname, 'verify_model.py'),
    modelId,
    filePath
  ], (error, stdout) => {
    if (error) {
        console.error(error);
        console.error('执行出错:', error);         // ← 加这一行
        console.error('标准错误输出:', stderr);   // ← 再加这一行
        return res.status(500).json({ error: '执行验证失败' });
    }
    try {
        const jsonStart = stdout.indexOf('{');
        const jsonEnd = stdout.lastIndexOf('}');
        const cleanJson = stdout.slice(jsonStart, jsonEnd + 1);
        const result = JSON.parse(cleanJson);
        res.json(result);
    } catch (e) {
        console.error('解析失败:', stdout);
        res.status(500).json({ error: 'JSON解析失败', raw: stdout });
    }

  });
});
