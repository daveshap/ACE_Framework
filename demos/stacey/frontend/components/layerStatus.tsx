import React, {useEffect, useState} from 'react';
import {io} from "socket.io-client";
import {Box, HStack, Spinner, Text, VStack} from "@chakra-ui/react";

interface LayerProps {
    layerId: number;
    displayName: string;
    backgroundColor: string;
}

export const LayerStatus: React.FC<LayerProps> = ({ layerId, displayName, backgroundColor }) => {
    const [status, setStatus] = useState('IDLE');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        console.error("NEXT_PUBLIC_BACKEND_URL is not set");
        return null;
    }

    const socket = io(backendUrl);

    useEffect(() => {
        socket.on(`layer-${layerId}-status`, (data) => {
            setStatus(data.status);
        });

        return () => {
            socket.off(`${layerId}-status`);
        };
    }, []);

    return (
        <Box width={300} bg={backgroundColor} p={4} justifyContent="space-between">
            <VStack>
                <Text fontSize={"lg"} fontWeight={"bold"}>{displayName}</Text>
                <HStack >
                    <Text fontSize={"sm"}>{status}</Text>
                    {status !== 'IDLE' && (
                        <Spinner thickness="4px" speed="0.65s" emptyColor="gray.200" color="blue.500" size="md" />
                    )}
                </HStack>
            </VStack>
        </Box>
    );
}

export default LayerStatus;
