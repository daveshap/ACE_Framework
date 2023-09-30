// Import required components from Chakra UI
import {Button, FormControl, FormLabel, Input, Radio, RadioGroup, Stack} from '@chakra-ui/react';
import {useState} from "react";

// Define the PublishMessageForm component
export const PublishMessageForm = () => {
    const [message, setMessage] = useState('');
    const [bus, setBus] = useState('northbound');
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
                bus: bus,
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
            <FormLabel>Message to Publish</FormLabel>
            <Input value={message} onChange={e => setMessage(e.target.value)} placeholder="Type your message" />

            <FormLabel>Bus</FormLabel>
            <RadioGroup value={bus} onChange={setBus}>
                <Stack direction="row">
                    <Radio value="northbound">Northbound</Radio>
                    <Radio value="southbound">Southbound</Radio>
                </Stack>
            </RadioGroup>

            <Button mt={4} colorScheme="teal" type="button" onClick={handleSubmit}>
                Publish Message
            </Button>
        </FormControl>
    );
};