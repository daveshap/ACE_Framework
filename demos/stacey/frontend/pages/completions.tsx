import React, {useEffect, useState} from 'react';
import {Alert, Heading, VStack} from '@chakra-ui/react';
import ChatCompletionComponent from "@/components/chatCompletion";


type GptMessage = {
    role: string;
    name?: string;
    content: string;
};

type ChatCompletion = {
    model: string;
    conversation: GptMessage[];
};

const LLMCompletions = () => {
    const [completions, setCompletions] = useState<ChatCompletion[]>([]);

    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }
    if (!socketUrl) {
        return <Alert status="error">I don't know where the socket backend is! Please set env variable NEXT_PUBLIC_SOCKET_URL</Alert>;
    }

    useEffect(() => {
        // Initial fetch of completions.
        fetch(backendUrl + '/llmlog')
            .then(res => res.json())
            .then(data => setCompletions(data));

        // Set up WebSocket for live updates.
        const ws = new WebSocket(socketUrl + '/ws-llmlog/')

        ws.onopen = () => {
            console.log('Connected to the WebSocket');
        };

        ws.onmessage = (event) => {
            const completion: ChatCompletion = JSON.parse(event.data);
            setCompletions(prev => [...prev, completion]);
        };

        ws.onclose = () => {
            console.log('Disconnected from the WebSocket');
        };

        return () => ws.close();

    }, []);

    return (
        <VStack backgroundColor="black" spacing={4} padding={4} align="start" width="100%" height="100vh" >
            <Heading color="white">LLM Completions</Heading>
            {completions.map((completion, index) => (
                <ChatCompletionComponent
                    key={index}
                    completion={completion}
                    showAssistantMessage={index === completions.length - 1}
                />
            ))}
        </VStack>
    );

}

export default LLMCompletions;
