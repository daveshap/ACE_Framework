// pages/component/Bus.tsx
import React, {useContext, useEffect, useState} from 'react';
import {Alert, Box, Button, Text, VStack} from '@chakra-ui/react';
import {PublishMessageForm} from "@/components/publish";
import BusMessage from "@/components/busMessage";
import {ArrowDownIcon, ArrowUpIcon} from "@chakra-ui/icons";
import {WebSocketContext, WebSocketEvent} from "@/context/WebSocketContext";

interface BusProps {
    busName: string;
}

interface MessageData {
    sender: string;
    message: string;
}

export const Bus: React.FC<BusProps> = ({ busName }) => {
    const [logs, setLogs] = useState<MessageData[]>([]);
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const socketEvent : WebSocketEvent | null = useContext(WebSocketContext);

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    useEffect(() => {
        if (socketEvent && socketEvent.eventType === 'bus-message' && socketEvent.data.bus === busName) {
            const messageData: MessageData = {
                sender: socketEvent.data.sender,
                message: socketEvent.data.message,
            };
            console.log('Received message:', messageData);
            setLogs((prevLogs) => [...prevLogs, messageData]);
        }
    }, [socketEvent, busName]);

    useEffect(() => {
        if (!backendUrl) return;

        fetch(backendUrl + `/bus?name=${busName}`)
            .then(response => response.json())
            .then(data => {
                console.log("Fetched logs:", data)
                setLogs(data)
            })
            .catch(error => console.error('Error fetching the logs:', error));
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
                    setLogs([]); // Clear the logs state on successful response
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
            <VStack spacing={4} w={500}>
                <Text fontSize="xl" mb={2}>🚌{arrowIcon} {`${busName} bus`} {arrowIcon}🚌</Text>
                <VStack align="start" spacing={1}>
                    {logs.map((log, index) => (
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
