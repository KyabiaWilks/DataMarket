// src/pages/Dashboard.jsx
import { useContext } from 'react';
import { Box, Heading, Text, VStack, Link } from '@chakra-ui/react';
import { AuthContext } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useContext(AuthContext);

  return (
    <Box>
      <VStack align="start" spacing={4}>
        <Heading>欢迎来到模型交易平台, {user?.username}!</Heading>
        <Text fontSize="lg">
          这是一个基于论文 <Link href="https://arxiv.org/abs/1805.08125" isExternal color="teal.500">《数据市场：一种算法解决方案》</Link> 复现的交互式平台。
        </Text>
        <Text>
          平台旨在通过一个安全、公平且高效的机制，解决数据作为一种独特经济商品所面临的挑战。
        </Text>
        <Text>
          您可以通过左侧的导航栏开始探索：
        </Text>
        <ul>
          <li><Text><b>市场 (Marketplace):</b> 浏览社区提供的、可用于您预测任务的各种模型和数据集。</Text></li>
          <li><Text><b>运行拍卖 (Run Auction):</b> 作为数据需求方，体验一次完整的、可视化的数据拍卖流程。</Text></li>
          <li><Text><b>我的模型 (My Models):</b> 作为数据提供方，注册并管理您的数据资产，并通过密码学方法验证其原创性。</Text></li>
          
        </ul>
      </VStack>
    </Box>
  );
};

export default Dashboard;