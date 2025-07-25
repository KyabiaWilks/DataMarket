// src/pages/Auth/Register.jsx
import {
  Box, Button, FormControl, FormLabel, Input, VStack, Heading, Text, Link as ChakraLink, useToast
} from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();
  const toast = useToast();

  const handleSubmit = (e) => {
    e.preventDefault();
    // 模拟注册逻辑
    toast({
      title: "注册成功",
      description: "您现在可以登录了。",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
    navigate('/login');
  };

  return (
    <Box display="flex" alignItems="center" justifyContent="center" height="100vh">
      <VStack as="form" onSubmit={handleSubmit} spacing={4} p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
        <Heading>注册</Heading>
        <FormControl isRequired>
          <FormLabel>用户名</FormLabel>
          <Input type="text" placeholder="输入您的用户名" />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>密码</FormLabel>
          <Input type="password" placeholder="输入您的密码" />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>确认密码</FormLabel>
          <Input type="password" placeholder="再次输入密码" />
        </FormControl>
        <Button type="submit" colorScheme="teal" width="full">注册</Button>
        <Text>
          已有账户? <ChakraLink as={RouterLink} to="/login" color="teal.500">点击登录</ChakraLink>
        </Text>
      </VStack>
    </Box>
  );
};

export default Register;