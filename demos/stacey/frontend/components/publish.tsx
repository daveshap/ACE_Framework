// pages/component/publish.tsx
import {Button, FormControl, Textarea} from '@chakra-ui/react';
import React, {useState} from "react";
import {TriangleDownIcon, TriangleUpIcon} from '@chakra-ui/icons'

interface PublishMessageFormProps {
    busType: string;
}

export const PublishMessageForm: React.FC<PublishMessageFormProps> = ({ busType }) => {
    const [message, setMessage] = useState('');
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || '';

    const handleSubmit = () => {
        fetch(backendUrl + '/publish_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender: 'admin web',
                message: message,
                bus: busType,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Message published:', data);
                setMessage(''); // Clear the message input field after successful submission
            })
            .catch(error => console.error('Error publishing the message:', error));
    };

    return (
        <FormControl as="form" onSubmit={handleSubmit}>
            <Textarea value={message} onChange={e => setMessage(e.target.value)} placeholder={`publish ${busType} message`} />
            <Button
                mt={4}
                colorScheme="teal"
                type="button"
                onClick={handleSubmit}
                size="sm" // Smaller size button
            >
                {busType === 'northbound' ? <TriangleUpIcon boxSize={4}/> : <TriangleDownIcon boxSize={4}/> }
            </Button>
        </FormControl>
    );
};