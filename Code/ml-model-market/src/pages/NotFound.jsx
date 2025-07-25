// src/pages/NotFound.jsx
import { Box, Heading, Text, Button } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <Box textAlign="center" py={10} px={6} height="100vh" display="flex" flexDirection="column" justifyContent="center">
      <Heading display="inline-block" as="h2" size="2xl" bg="teal.400" backgroundClip="text">
        404
      </Heading>
      <Text fontSize="18px" mt={3} mb={2}>
        页面未找到
      </Text>
      <Text color={'gray.500'} mb={6}>
        您要查找的页面似乎不存在。
      </Text>
      <Button
        as={Link}
        to="/"
        colorScheme="teal"
        bgGradient="linear(to-r, teal.400, teal.500, teal.600)"
        color="white"
        variant="solid">
        返回首页
      </Button>
    </Box>
  );
};

export default NotFound;