// pages/component/Bus.tsx
import React, {useEffect, useState} from 'react';
import {Box, Text, VStack} from '@chakra-ui/react';
import {PublishMessageForm} from "@/components/publish";

interface BusProps {
    busName: string;
}

export const Bus: React.FC<BusProps> = ({ busName }) => {
    const [logs, setLogs] = useState([]);
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    useEffect(() => {
        if (!backendUrl) return;

        fetch(backendUrl + `/bus?name=${busName}`)
            .then(response => response.json())
            .then(data => setLogs(data))
            .catch(error => console.error('Error fetching the logs:', error));
    }, []);

    return (
        <Box p={4}>
            <VStack spacing={4}>
                <Text fontSize="xl" mb={2}>{`${busName} bus`}</Text>
                <VStack align="start" spacing={1}>
                    {logs.map((log, index) => (
                        <Text key={index}>{JSON.stringify(log)}</Text>
                    ))}
                </VStack>
                <PublishMessageForm busType={busName}/>
            </VStack>
        </Box>
    );
};
