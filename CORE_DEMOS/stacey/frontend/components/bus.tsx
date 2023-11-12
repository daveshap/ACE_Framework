// pages/component/Bus.tsx
import React, {useEffect, useRef, useState} from 'react';
import {Alert, Box, Button, Text, VStack} from '@chakra-ui/react';
import {PublishMessageForm} from "@/components/publish";
import BusMessage from "@/components/busMessage";
import {ArrowDownIcon, ArrowUpIcon} from "@chakra-ui/icons";

interface BusProps {
    busName: string;
}

interface MessageData {
    sender: string;
    message: string;
}

export const Bus: React.FC<BusProps> = ({ busName }) => {
    const [messages, setMessages] = useState<MessageData[]>([]);
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL
    const webSocketRef = useRef<WebSocket | null>(null);  // New WebSocket reference

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }
    if (!socketUrl) {
        return <Alert status="error">I don't know where the socket backend is! Please set env variable NEXT_PUBLIC_SOCKET_URL</Alert>;
    }

    useEffect(() => {
        if (!backendUrl) return;

        fetch(backendUrl + `/bus?name=${busName}`)
            .then(response => response.json())
            .then(data => {
                console.log("Fetched logs:", data)
                setMessages(data)
            })
            .catch(error => console.error('Error fetching the logs:', error));

        // Create WebSocket connection
        webSocketRef.current = new WebSocket(`${socketUrl}/ws-bus/${busName}/`);

        webSocketRef.current.onopen = (event: Event) => {
            console.log(`WebSocket for ${busName} opened:`, event);
        };

        // Set up listeners
        webSocketRef.current.onmessage = (event: MessageEvent) => {
            const data = JSON.parse(event.data);
            if (data.eventType === 'busMessage' && data.data.bus === busName) {
                const messageData: MessageData = {
                    sender: data.data.sender,
                    message: data.data.message,
                };
                console.log('Received message:', messageData);
                setMessages((prevLogs) => [...prevLogs, messageData]);
            }
        };

        webSocketRef.current.onerror = (error: Event) => {
            console.error(`WebSocket error for ${busName}:`, error);
        };

        // Clean up the connection when component is unmounted
        return () => {
            if (webSocketRef.current) {
                webSocketRef.current.close();
                console.log(`WebSocket for ${busName} closed.`);
            }
        };
    }, [backendUrl, busName]);

    const clearMessages = () => {
        fetch(backendUrl + '/clear_messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ bus: busName }),
        })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    setMessages([]); // Clear the logs state on successful response
                    console.log(data.message);
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error clearing the messages:', error));
    };

    const arrowIcon = busName === "northbound" ? <ArrowUpIcon boxSize={6} /> : <ArrowDownIcon boxSize={6} />
    const background = busName === "northbound" ? "pink.100" : "purple.100"

    return (
        <Box p={4} background={background} rounded={10}>
            <VStack spacing={4}>
                <Text fontSize="xl" mb={2}>🚌{arrowIcon} {`${busName} bus`} {arrowIcon}🚌</Text>
                <VStack align="start" spacing={1}>
                    {messages.map((log, index) => (
                        <BusMessage key={index} sender={log.sender} message={log.message} />
                    ))}
                </VStack>
                <PublishMessageForm busType={busName}/>
                <Text fontSize="xl" mb={2}>🚌{arrowIcon} {`${busName} bus`} {arrowIcon}🚌</Text>
                <Button size={"sm"} onClick={clearMessages} colorScheme="red">Clear Messages</Button>
            </VStack>
        </Box>
    );
};
