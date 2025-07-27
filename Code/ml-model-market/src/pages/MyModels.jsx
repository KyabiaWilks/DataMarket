// src/pages/MyModels.jsx
import { useState } from 'react';
import {
  Box,
  Heading,
  Button,
  VStack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Tag,
  useToast,
  Text,
  Flex,
  Icon,
  FormControl,
  FormLabel,
  Input,
} from '@chakra-ui/react';

import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from '@chakra-ui/react';

import { MdCloudUpload, MdCheckCircle, MdHourglassEmpty } from 'react-icons/md';

const MyModels = () => {
  const [myModels, setMyModels] = useState([
    { id: 'seller-model-01', name: '我的客流量时间序列数据', status: '已验证', hash: 'a1b2c3d4e5f6' },
    { id: 'seller-model-02', name: '地区销售额数据集', status: '已验证', hash: 'f6g7h8i9j0k1' },
  ]);

  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();
  const [isUploading, setIsUploading] = useState(false);
  const [newModelName, setNewModelName] = useState('');
  const [file, setFile] = useState(null);
  
  const handleRegisterModel = async () => {
    if (!newModelName || !file) {
      toast({ title: "请填写完整信息", status: "warning", duration: 3000 });
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    const newId = `seller-model-0${myModels.length + 1}`;

    formData.append('modelId', newId);
    formData.append('modelName', newModelName);
    formData.append('bid', 200); // 可拓展为用户输入
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:3001/api/verify-model', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('验证失败');
      const result = await response.json();

      setMyModels([
        ...myModels,
        {
          id: newId,
          name: newModelName,
          status: '已验证',
          hash: result.data_hash || '未知',
          gain: result.prediction_gain_achieved,
          price: result.market_price_offered
        }
      ]);

      toast({
        title: "验证成功",
        description: `ZKP 验证成功，模型已登记。预测增益为 ${result.prediction_gain_achieved}`,
        status: "success",
        duration: 5000
      });

      setNewModelName('');
      setFile(null);
      onClose();
    } catch (err) {
      console.error(err);
      toast({
        title: "验证失败",
        description: "服务器返回错误，请检查数据格式或稍后重试。",
        status: "error",
        duration: 5000
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading>我的模型/数据</Heading>
        <Button leftIcon={<MdCloudUpload />} colorScheme="teal" onClick={onOpen}>
          注册新模型
        </Button>
      </Flex>

      {/* 直接使用 Box 包裹表格 */}
      <Box overflowX="auto">
        <Table variant='simple'>
          <Thead>
            <Tr>
              <Th>模型/数据名称</Th>
              <Th>状态</Th>
              <Th>数据哈希 (已验证)</Th>
            </Tr>
          </Thead>
          <Tbody>
            {myModels.map(model => (
              <Tr key={model.id}>
                <Td>{model.name}</Td>
                <Td>
                  <Tag colorScheme={model.status === '已验证' ? 'green' : 'yellow'}>
                    <Icon
                      as={model.status === '已验证' ? MdCheckCircle : MdHourglassEmpty}
                      mr={2}
                    />
                    {model.status}
                  </Tag>
                </Td>
                <Td fontFamily="monospace">{model.hash}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>注册新的数据/模型</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>名称</FormLabel>
                <Input
                  placeholder="例如：我的店铺销售数据"
                  value={newModelName}
                  onChange={(e) => setNewModelName(e.target.value)}
                />
              </FormControl>
              <FormControl isRequired>
                <FormLabel>数据文件</FormLabel>
                <Input type="file" p={1} onChange={(e) => setFile(e.target.files[0])} />
                <Text fontSize="sm" color="gray.500" mt={1}>
                  上传后，系统将生成数据哈希并创建零知识证明以验证原创性。
                </Text>
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant='ghost' mr={3} onClick={onClose}>取消</Button>
            <Button colorScheme='teal' onClick={handleRegisterModel} isLoading={isUploading}>
              提交验证
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default MyModels;
