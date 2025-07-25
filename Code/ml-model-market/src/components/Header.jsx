// src/components/Header.jsx
import { useContext } from 'react';
import { Box, Flex, Text, Button, Avatar } from '@chakra-ui/react';
import { AuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error("登出失败:", error);
    }
  };

  return (
    <Flex
      as="header"
      align="center"
      justify="flex-end"
      w="100%"
      px="4"
      py="2"
      bg="white"
      borderBottomWidth="1px"
      borderColor="gray.200"
    >
      {user && (
        <Flex align="center">
          <Avatar size="sm" name={user.username} mr="2" />
          <Text mr="4">欢迎, {user.username}</Text>
          <Button colorScheme="teal" variant="outline" size="sm" onClick={handleLogout}>
            登出
          </Button>
        </Flex>
      )}
    </Flex>
  );
};

export default Header;