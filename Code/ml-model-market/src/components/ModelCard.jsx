// src/components/ModelCard.jsx
import { Card, CardHeader, CardBody, Heading, Text, Button } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const ModelCard = ({ model }) => {
  const navigate = useNavigate();

  return (
    <Card>
      <CardHeader>
        <Heading size='md'>{model.name}</Heading>
      </CardHeader>
      <CardBody>
        <Text>{model.description}</Text>
        <Button mt={4} colorScheme="teal" onClick={() => navigate('/run-auction')}>
          使用此模型进行拍卖
        </Button>
      </CardBody>
    </Card>
  );
};

export default ModelCard;