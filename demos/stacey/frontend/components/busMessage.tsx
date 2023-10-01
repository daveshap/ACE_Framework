import {Box, Text} from '@chakra-ui/react';
import React from 'react';

interface BusMessageProps {
    sender: string;
    message: string;
}

const BusMessage: React.FC<BusMessageProps> = ({ sender, message }) => (
    <Box bg="gray.300" p={3} borderRadius="md" w="full" boxShadow="sm">
        <Text fontWeight="bold" mb={1}>{sender}:</Text>
        <Text>{message}</Text>
    </Box>
);

export default BusMessage;
