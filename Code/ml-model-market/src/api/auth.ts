// src/api/auth.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:3001/api', // 模拟后端的地址
  withCredentials: true, // 允许跨域携带 cookie
});

export default {
  login(credentials: any) {
    return apiClient.post('/login', credentials);
  },
  logout() {
    return apiClient.post('/logout');
  },
  getProfile() {
    return apiClient.get('/profile');
  },
  runAuction(data: { modelId: string; bid: any; taskData: any; }) {
    return apiClient.post('/run-auction', data);
  }
};
