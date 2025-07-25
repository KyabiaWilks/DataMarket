// src/router/index.jsx
import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import MainLayout from '../layouts/MainLayout';

// 私有路由守卫
export const PrivateRoutes = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);

  if (loading) {
    return <div>加载中...</div>; // 或者一个加载动画
  }

  return isAuthenticated? (
    <MainLayout>
      <Outlet />
    </MainLayout>
  ) : (
    <Navigate to="/login" />
  );
};

// 公开路由守卫
export const PublicRoutes = () => {
    const { isAuthenticated, loading } = useContext(AuthContext);

    if (loading) {
        return <div>加载中...</div>;
    }

    return isAuthenticated? <Navigate to="/" /> : <Outlet />;
}