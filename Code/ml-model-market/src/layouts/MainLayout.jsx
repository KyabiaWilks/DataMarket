// src/layouts/MainLayout.jsx
import { Box, Flex } from '@chakra-ui/react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

const MainLayout = ({ children }) => {
  return (
    <Flex>
      <Sidebar />
      <Box flex="1">
        <Header />
        <Box p="4">
          {children}
        </Box>
      </Box>
    </Flex>
  );
};

export default MainLayout;