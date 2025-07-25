// src/pages/Marketplace.jsx
import { Box, Heading, Text, SimpleGrid } from '@chakra-ui/react';
import ModelCard from '../components/ModelCard';

const Marketplace = () => {
  // 模拟从后端获取的模型列表
  const models = [
    { id: 'model-123', name: '房价预测回归模型', description: '基于波士顿房价数据集训练，预测房屋中位数价值。' },
    { id: 'model-456', name: '客户流失分类模型', description: '预测电信客户是否会流失，适用于分类任务。' },
    { id: 'model-789', name: '库存需求时间序列模型', description: '基于历史销售数据，预测未来库存需求。' },
    { id: 'model-abc', name: '医疗影像诊断辅助模型', description: '需要“认证医疗研究员”凭证方可访问。' },
    { id: 'model-def', name: '金融市场情绪分析', description: '分析新闻和社交媒体数据以预测市场情绪。' },
    { id: 'model-ghi', name: '零售客流量数据集', description: '包含多家零售店的匿名化分钟级客流量数据。' },
  ];

  return (
    <Box>
      <Heading mb={2}>模型市场</Heading>
      <Text mb={6} color="gray.600">在这里浏览可用于您预测任务的各种模型和数据集。</Text>
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
        {models.map((model) => (
          <ModelCard key={model.id} model={model} />
        ))}
      </SimpleGrid>
    </Box>
  );
};

export default Marketplace;