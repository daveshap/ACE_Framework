// pages/chat.tsx
import React, {useEffect, useRef, useState} from 'react';
import axios from 'axios';
import {Alert, Box, Container, Flex, Heading, Image, Select, Spinner, Text, Textarea, VStack} from '@chakra-ui/react';
import ChakraUIRenderer from "chakra-ui-markdown-renderer";
import ReactMarkdown from "react-markdown";
import {ChatMessage, createChatMessage} from "@/lib/types";

const userName = 'web-user'

function Chat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [model, setModel] = useState('gpt-4');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const chatSocketUrl = process.env.NEXT_PUBLIC_SOCKET_URL;
    const webSocketRef = useRef<WebSocket | null>(null);
    const [userName, setUserName] = useState('web-user');


    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }
    if (!chatSocketUrl) {
        return <Alert status="error">I don't know where the chat socket backend is! Please set env variable NEXT_PUBLIC_CHAT_SOCKET_URL</Alert>;
    }

    function add_message(incomingMessage: ChatMessage) {
        setMessages(prevMessages => [...prevMessages, incomingMessage]);
    }

    useEffect(() => {
        // Initialize WebSocket connection
        webSocketRef.current = new WebSocket(chatSocketUrl + "/ws-chat/");

        // Define event handlers
        webSocketRef.current.onopen = (event) => {
            console.log('WebSocket open:', event);
        };

        webSocketRef.current.onmessage = (event) => {
            const incomingMessage: ChatMessage = JSON.parse(event.data);
            add_message(incomingMessage);
        };

        webSocketRef.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        webSocketRef.current.onclose = (event) => {
            console.log('WebSocket closed:', event);
        };

        // Cleanup: close the WebSocket connection when the component is unmounted
        return () => {
            if (webSocketRef.current) {
                webSocketRef.current.close();
            }
        };
    }, []);  // Empty dependency array means this useEffect runs once, similar to componentDidMount


    const handleKeyPress = async (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const newMessage = createChatMessage(userName, input);
            const updatedMessages = [...messages, newMessage];
            setMessages(updatedMessages);
            setLoading(true);
            setInput('');

            try {
                const response = await axios.post(backendUrl + "/chat", {
                    model: model,
                    messages: updatedMessages,
                });
                console.log('Response from backend:', response)
                if (response.data?.content) {
                    add_message(response.data)
                }

            } catch (error) {
                console.error('Error sending message:', error);
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <Container p={4} backgroundColor="white">
            <VStack spacing={4} align="stretch" h="full">
                <Heading mb={4}>Stacey chat</Heading>
                <Box flex="1" overflowY="auto" p={3}>
                    {messages.map((msg, index) => (
                        <Flex key={index} mb={2} direction="column" align={msg.sender === userName ? 'flex-end' : 'flex-start'}>
                            <Flex align="center">
                                {msg.sender === 'Stacey' && <Image src="/images/stacey-160.png" borderRadius="full" boxSize="40px" mr={2} />}
                                <Box p={2} rounded="md" bg={msg.sender === userName ? 'blue.100' : 'gray.100'}>
                                    <Text><b>{msg.sender === userName ? 'You' : msg.sender}:</b></Text>
                                    <ReactMarkdown  components={ChakraUIRenderer()} skipHtml>
                                        {msg.content}
                                    </ReactMarkdown>
                                </Box>
                            </Flex>
                        </Flex>
                    ))}
                </Box>
                {loading ? <Spinner /> :
                    <>
                        <Textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyPress}
                            h="60px"
                            placeholder="Say something..."
                        />
                        <Flex mt={2} align="center">
                            <Text mr={2}>User Name:</Text>
                            <input
                                type="text"
                                value={userName}
                                onChange={(e) => setUserName(e.target.value)}
                                placeholder="web-user"
                            />
                        </Flex>
                        <Select
                            mb={4}
                            placeholder="Select model"
                            value={model}
                            onChange={(e) => setModel(e.target.value)}
                        >
                            <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
                            <option value="gpt-4">gpt-4</option>
                        </Select>
                    </>

                }
            </VStack>
        </Container>
    );
}

export default Chat;
