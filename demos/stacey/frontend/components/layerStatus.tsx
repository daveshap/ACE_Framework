import React, {useEffect, useState} from 'react';
import {io} from "socket.io-client";
import {Spinner} from "@chakra-ui/react";

function LayerStatus() {
    const [status, setStatus] = useState('IDLE');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        console.error("NEXT_PUBLIC_BACKEND_URL is not set");
        return null;
    }

    const socket = io(backendUrl);

    useEffect(() => {
        socket.on('status', (data) => {
            setStatus(data.status);
        });

        return () => {
            socket.off('status');
        };
    }, []);

    return (
        status !== 'IDLE' && (
            <Spinner thickness="4px" speed="0.65s" emptyColor="gray.200" color="blue.500" size="xl" />
        )
    );
}

export default LayerStatus;
