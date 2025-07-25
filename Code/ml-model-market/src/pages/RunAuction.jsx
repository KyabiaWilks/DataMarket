// src/pages/RunAuction.jsx
import { useState } from 'react';
import {
  Box, Heading, VStack, FormControl, FormLabel, Input, Button, Spinner, Text, SimpleGrid, Stat, StatLabel, StatNumber, Code
} from '@chakra-ui/react';
import api from '../api/auth';

const RunAuction = () => {
  const [bid, setBid] = useState(200);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleRunAuction = async () => {
    setIsLoading(true);
    setResults(null);
    try {
      const response = await api.runAuction({ modelId: 'model-123', bid });
      setResults(response.data);
    } catch (error) {
      console.error("拍卖失败:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Heading mb={6}>运行一次完整的拍卖流程</Heading>
      <VStack spacing={4} align="stretch" maxW="600px">
        <FormControl>
          <FormLabel>选择模型/数据集</FormLabel>
          <Input value="默认回归模型 (ID: model-123)" isReadOnly />
        </FormControl>
        <FormControl>
          <FormLabel>上传您的预测任务 (Y_task)</FormLabel>
          <Input type="file" p={1} />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>您的出价 (μ_n)</FormLabel>
          <Input type="number" value={bid} onChange={(e) => setBid(e.target.value)} />
        </FormControl>
        <Button colorScheme="teal" onClick={handleRunAuction} isLoading={isLoading}>
          开始拍卖
        </Button>
      </VStack>

      {isLoading && <Spinner mt={8} />}

      {results && (
        <Box mt={8} p={5} borderWidth={1} borderRadius="lg">
          <Heading size="md" mb={4}>拍卖结果</Heading>
          <SimpleGrid columns={2} spacing={6}>
            <Stat>
              <StatLabel>第1步: 市场定价 (p_n)</StatLabel>
              <StatNumber>${results.market_price_offered}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>第2步: 您的出价 (b_n)</StatLabel>
              <StatNumber>${results.your_bid}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>第3步: 预测增益 (G)</StatLabel>
              <StatNumber>{results.prediction_gain_achieved}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>第4步: 您的费用 (r_n)</StatLabel>
              <StatNumber color="red.500">${results.cost_to_you}</StatNumber>
            </Stat>
          </SimpleGrid>
          <Box mt={6}>
            <Heading size="sm" mb={2}>第5步: 收益分配 (Shapley Values)</Heading>
            <Code p={4} borderRadius="md" width="100%">
              <pre>{JSON.stringify(results.seller_payouts, null, 2)}</pre>
            </Code>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default RunAuction;