// components/layerStatus.tsx
import React, {useContext, useEffect, useState} from 'react';
import {Box, HStack, Spinner, Text, VStack} from "@chakra-ui/react";
import {WebSocketContext, WebSocketEvent} from "@/context/WebSocketContext";

interface LayerProps {
    layerId: number;
    displayName: string;
    backgroundColor: string;
}

export const LayerStatus: React.FC<LayerProps> = ({ layerId, displayName, backgroundColor }) => {
    const [status, setStatus] = useState('IDLE');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const socketEvent : WebSocketEvent | null = useContext(WebSocketContext);

    if (!backendUrl) {
        console.error("NEXT_PUBLIC_BACKEND_URL is not set");
        return null;
    }

    useEffect(() => {
        if (socketEvent && socketEvent.eventType === 'layer-status' && socketEvent.data.layerId === layerId) {
            setStatus(socketEvent.data.status);
        }
    }, [socketEvent, layerId]);

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
