import { useState } from 'react';
import axios from 'axios';
import { Box, Textarea, VStack, Text, Container, Alert, Heading, Flex } from '@chakra-ui/react';

function Chat() {
    const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
    const [input, setInput] = useState('');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    const handleKeyPress = async (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            setMessages([...messages, { role: 'user', content: input }]);

            try {
                const response = await axios.post(backendUrl + "/chat", {
                    model: 'gpt-3.5-turbo',
                    conversation: [...messages, { role: 'user', content: input }],
                });

                setMessages([...messages, { role: 'user', content: input }, response.data]);
            } catch (error) {
                console.error('Error sending message:', error);
            }

            setInput('');
        }
    };

    return (
        <Container maxW="container.md" p={4}>
            <VStack spacing={4} align="stretch" h="full">
                <Heading mb={4}>Stacey</Heading>
                <Box flex="1" overflowY="auto" p={3}>
                    {messages.map((msg, index) => (
                        <Flex key={index} mb={2} direction="column" align={msg.role === 'user' ? 'flex-end' : 'flex-start'}>
                            <Box p={2} rounded="md" bg={msg.role === 'user' ? 'blue.100' : 'gray.100'}>
                                <Text>
                                    <b>{msg.role === 'user' ? 'You' : 'Stacey'}:</b> {msg.content}
                                </Text>
                            </Box>
                        </Flex>
                    ))}
                </Box>
                <Textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    h="60px"
                    placeholder="Say something..."
                />
            </VStack>
        </Container>
    );
}

export default Chat;
