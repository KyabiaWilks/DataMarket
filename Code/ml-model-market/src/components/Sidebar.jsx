// src/components/Sidebar.jsx
import { Box, VStack, Link as ChakraLink, Heading } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import { MdDashboard, MdStore, MdAccountBalanceWallet, MdPlayCircleFilled } from 'react-icons/md';

const Sidebar = () => {
  const navItems = [
    { label: '首页', path: '/', icon: MdDashboard },
    { label: '模型市场', path: '/marketplace', icon: MdStore },
    { label: '运行拍卖', path: '/run-auction', icon: MdAccountBalanceWallet },
    { label: '我的模型', path: '/my-models', icon: MdPlayCircleFilled },
  ];

  return (
    <Box w="250px" h="100vh" bg="gray.100" p="4" borderRight="1px" borderColor="gray.200">
      <Heading size="md" mb="8">模型交易平台</Heading>
      <VStack align="stretch" spacing={4}>
        {navItems.map((item) => (
          <ChakraLink as={RouterLink} to={item.path} key={item.label} display="flex" alignItems="center" p={2} borderRadius="md" _hover={{ bg: 'gray.200' }}>
            <item.icon style={{ marginRight: '8px' }} />
            {item.label}
          </ChakraLink>
        ))}
      </VStack>
    </Box>
  );
};

export default Sidebar;