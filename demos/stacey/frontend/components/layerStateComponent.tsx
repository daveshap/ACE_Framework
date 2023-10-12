// components/layerState.tsx
// noinspection JSIgnoredPromiseFromCall

import React, {useEffect, useRef, useState} from 'react';
import {Alert, Box, Spinner, Text, VStack} from "@chakra-ui/react";
import ReactMarkdown from "react-markdown";
import ChakraUIRenderer from "chakra-ui-markdown-renderer";

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
    const [countdown, setCountdown] = useState(null);  // state for countdown timer

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }
    if (!socketUrl) {
        return <Alert status="error">I don't know where the socket backend is! Please set env variable NEXT_PUBLIC_SOCKET_URL</Alert>;
    }

    const computeCountdown = (nextWakeupTime: string) => {
        const endTime = new Date(nextWakeupTime).getTime();
        const now = new Date().getTime();
        return Math.floor((endTime - now) / 1000); // convert to seconds and round down
    }

    useEffect(() => {
        // Fetch the initial layerState
        async function fetchInitialLayerState() {
            try {
                const response = await fetch(`${backendUrl}/layer_state/${layerId}/`);
                console.log("response", response);
                const initialState = await response.json();
                console.log("response.json", initialState);

                // Initialize countdown timer if next_wakeup_time is set
                if (initialState.next_wakeup_time) {
                    const endTime = new Date(initialState.next_wakeup_time).getTime();
                    const now = new Date().getTime();
                    const duration = endTime - now;
                    setCountdown(duration / 1000); // convert to seconds
                }

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
        if (layerState?.next_wakeup_time) {
            setCountdown(computeCountdown(layerState.next_wakeup_time));
        }

        // Logic to update the countdown timer
        const timer = setInterval(() => {
            if (layerState?.next_wakeup_time) {
                const newCountdown = computeCountdown(layerState.next_wakeup_time);
                setCountdown(newCountdown > 0 ? newCountdown : null);
            }
        }, 1000);

        // Cleanup logic
        return () => {
            clearInterval(timer); // clear the timer
        };
    }, [backendUrl, layerId, layerState?.next_wakeup_time]);

    useEffect(() => {
        // Update the countdown timer when layerState.next_wakeup_time changes
        if (layerState?.next_wakeup_time) {
            const endTime = new Date(layerState.next_wakeup_time).getTime();
            const now = new Date().getTime();
            const duration = endTime - now;
            setCountdown(duration / 1000); // convert to seconds
        } else {
            setCountdown(null);
        }
    }, [layerState?.next_wakeup_time]);

    return (
        <Box bg={backgroundColor} p={4} justifyContent="space-between">
            <VStack>
                <Text fontSize={"lg"} fontWeight={"bold"}>{displayName}</Text>
                <VStack>
                    {layerState?.whiteboard && (
                        <Box p={4} bg="white" borderRadius="md" borderColor="gray.200" borderWidth={2} width="full" whiteSpace="pre-line">
                            <ReactMarkdown components={ChakraUIRenderer()}>{layerState.whiteboard}</ReactMarkdown>
                        </Box>
                    )}
                    {layerState?.active && (
                        <Spinner size="xl" />
                    )}
                    {layerState?.next_wakeup_time && (
                        <>
                            <Text fontSize={"sm"} fontWeight="bold">Next Wakeup Time</Text>
                            <Text fontSize={"sm"}>{layerState.next_wakeup_time} ({countdown} sec)</Text>
                        </>
                    )}
                </VStack>
            </VStack>
        </Box>
    );
}


export default LayerStateComponent;
