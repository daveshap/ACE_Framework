// pages/busLogs.tsx
import React, {useEffect, useState} from 'react';
import {Alert, Box, Text, VStack} from '@chakra-ui/react';
import {PublishMessageForm} from "@/pages/admin/publishMessage";

const BusLogsPage = () => {
    const [logs, setLogs] = useState({ northbound: [], southbound: [] });
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    useEffect(() => {
        // Replace with your Flask app URL
        fetch( backendUrl + '/bus_logs')
            .then(response => response.json())
            .then(data => setLogs(data))
            .catch(error => console.error('Error fetching the logs:', error));
    }, []);

    return (
        <Box p={4}>
            <VStack spacing={4}>
                <PublishMessageForm />
                <Box>
                    <Text fontSize="xl" mb={2}>Northbound Bus Logs:</Text>
                    <VStack align="start" spacing={1}>
                        {logs.northbound.map((log, index) => (
                            <Text key={index}>{JSON.stringify(log)}</Text>
                        ))}
                    </VStack>
                </Box>

                <Box>
                    <Text fontSize="xl" mb={2}>Southbound Bus Logs:</Text>
                    <VStack align="start" spacing={1}>
                        {logs.southbound.map((log, index) => (
                            <Text key={index}>{JSON.stringify(log)}</Text>
                        ))}
                    </VStack>
                </Box>
            </VStack>
        </Box>
    );
};

export default BusLogsPage;
