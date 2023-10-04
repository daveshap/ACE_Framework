// context/WebSocketContext.js
import React, {createContext, ReactNode, useEffect, useState} from 'react';

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

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:5000/ws/');

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
