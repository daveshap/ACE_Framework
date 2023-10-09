// components/layerState.tsx
// noinspection JSIgnoredPromiseFromCall

import React, {useEffect, useRef, useState} from 'react';
import {Alert, Box, Text, VStack} from "@chakra-ui/react";

interface LayerProps {
    layerId: number;
    displayName: string;
    backgroundColor: string;
}

export const LayerStateComponent: React.FC<LayerProps> = ({ layerId, displayName, backgroundColor }) => {
    const [layerState, setLayerState] = useState(null);
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
        // Fetch the initial layerState
        async function fetchInitialLayerState() {
            try {
                const response = await fetch(`${backendUrl}/layer_state/${layerId}/`);
                console.log("response", response);
                const initialState = await response.json();
                console.log("response.json", initialState);
                setLayerState(initialState);
            } catch (error) {
                console.error(`Error fetching initial layer state for ${layerId}:`, error);
            }
        }

        fetchInitialLayerState();

        // Initialize the WebSocket connection
        webSocketRef.current = new WebSocket(`${socketUrl}/ws-layer/${layerId}/`);

        // Handle incoming messages
        webSocketRef.current.onmessage = (event: MessageEvent) => {
            const layer_state = JSON.parse(event.data);
            setLayerState(layer_state);
        };

        webSocketRef.current.onerror = (error: Event) => {
            console.error(`WebSocket error for layer ${layerId}:`, error);
        };

        // Cleanup logic (close the WebSocket when the component is unmounted)
        return () => {
            if (webSocketRef.current) {
                webSocketRef.current.close();
            }
        };
    }, [backendUrl, layerId]);

    return (
        <Box width={300} bg={backgroundColor} p={4} justifyContent="space-between">
            <VStack>
                <Text fontSize={"lg"} fontWeight={"bold"}>{displayName}</Text>
                <VStack>
                    {layerState && Object.entries(layerState).map(([key, value]) => (
                        <Text key={key} fontSize={"sm"}>{key}: {value ? value.toString() : 'null'}</Text>
                    ))}
                </VStack>
            </VStack>
        </Box>
    );
}


export default LayerStateComponent;
