// pages/component/Bus.tsx
import React, {useEffect, useState} from 'react';
import {Alert, Box, Text, VStack} from '@chakra-ui/react';
import {PublishMessageForm} from "@/components/publish";
import io from 'socket.io-client';
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
    const [logs, setLogs] = useState<MessageData[]>([]);
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    useEffect(() => {
        const socket = io(backendUrl);
        console.log('Connected to socket.io server')
        socket.on(busName, (data: MessageData) => {
            console.log('Received message:', data)
            setLogs((prevLogs) => [...prevLogs, data]);
        });

        return () => {
            socket.disconnect();
        };
    }, [busName, backendUrl]);

    useEffect(() => {
        if (!backendUrl) return;

        fetch(backendUrl + `/bus?name=${busName}`)
            .then(response => response.json())
            .then(data => {
                console.log("Fetched logs:", data)
                setLogs(data)
            })
            .catch(error => console.error('Error fetching the logs:', error));
    }, []);

    const arrowIcon = busName === "northbound" ? <ArrowUpIcon boxSize={6} /> : <ArrowDownIcon boxSize={6} />
    const background = busName === "northbound" ? "pink.100" : "purple.100"

    return (
        <Box p={4} background={background} rounded={10}>
            <VStack spacing={4} w={500}>
                <Text fontSize="xl" mb={2}>{arrowIcon} {`${busName} bus`} {arrowIcon}</Text>
                <VStack align="start" spacing={1}>
                    {logs.map((log, index) => (
                        <BusMessage key={index} sender={log.sender} message={log.message} />
                    ))}
                </VStack>
                <PublishMessageForm busType={busName}/>
                <Text fontSize="xl" mb={2}>{arrowIcon} {`${busName} bus`} {arrowIcon}</Text>
            </VStack>
        </Box>
    );
};
