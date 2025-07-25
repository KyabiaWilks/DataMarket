// src/App.jsx
import { Routes, Route } from 'react-router-dom';
import { PrivateRoutes, PublicRoutes } from './router';

// 导入页面组件
import Dashboard from './pages/Dashboard';
import Marketplace from './pages/Marketplace';
import MyModels from './pages/MyModels';
import RunAuction from './pages/RunAuction';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import NotFound from './pages/NotFound.jsx';

function App() {
  return (
    <Routes>
      {/* 私有路由 */}
      <Route element={<PrivateRoutes />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/marketplace" element={<Marketplace />} />
        <Route path="/my-models" element={<MyModels />} />
        <Route path="/run-auction" element={<RunAuction />} />
      </Route>

      {/* 公开路由 */}
      <Route element={<PublicRoutes />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>
      
      {/* 404 页面 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;