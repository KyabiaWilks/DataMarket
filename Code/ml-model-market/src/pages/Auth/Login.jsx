// src/pages/Auth/Login.jsx
import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import {
  Box, Button, FormControl, FormLabel, Input, VStack, Heading, useToast
} from '@chakra-ui/react';

const Login = () => {
  const [username, setUsername] = useState('testuser');
  const [password, setPassword] = useState('password123');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/');
      toast({ title: "登录成功", status: "success", duration: 3000, isClosable: true });
    } catch (error) {
      toast({ title: "登录失败", description: "请检查您的用户名和密码", status: "error", duration: 3000, isClosable: true });
    }
  };

  return (
    <Box display="flex" alignItems="center" justifyContent="center" height="100vh">
      <VStack as="form" onSubmit={handleSubmit} spacing={4} p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
        <Heading>登录</Heading>
        <FormControl isRequired>
          <FormLabel>用户名</FormLabel>
          <Input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>密码</FormLabel>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </FormControl>
        <Button type="submit" colorScheme="teal" width="full">登录</Button>
      </VStack>
    </Box>
  );
};

export default Login;