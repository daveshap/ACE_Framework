// context/WebSocketContext.js
import React, {createContext, ReactNode, useEffect, useState} from 'react';
import {Alert} from "@chakra-ui/react";

export interface WebSocketEvent {
    eventType: string;
    data: any;  // Replace with a more specific type if possible.
}

export const WebSocketContext = createContext<WebSocketEvent | null>(null);

interface WebSocketProviderProps {
    children: ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
    const [socketEvent, setSocketEvent] = useState<WebSocketEvent | null>(null);
    const adminSocketUrl = process.env.NEXT_PUBLIC_ADMIN_SOCKET_URL;
    if (!adminSocketUrl) {
        return <Alert status="error">I don't know where the admin socket backend is! Please set env variable NEXT_PUBLIC_ADMIN_SOCKET_URL</Alert>;
    }

    useEffect(() => {
        const socket = new WebSocket(adminSocketUrl);

        socket.onmessage = (event) => {
            console.log("WebSocketProvider got event:", event.data)
            const parsedData = JSON.parse(event.data);
            setSocketEvent(parsedData);
        };

        return () => socket.close();
    }, []);

    return (
        <WebSocketContext.Provider value={socketEvent}>
            {children}
        </WebSocketContext.Provider>
    );
};
