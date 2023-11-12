import React, {useEffect, useState} from 'react';
import {Box, Button, Collapse, Text} from '@chakra-ui/react';

type GptMessage = {
    role: string;
    name?: string;
    content: string;
};

type ChatCompletionProps = {
    completion: {
        model: string;
        conversation: GptMessage[];
    };
};

const ChatCompletionComponent: React.FC<ChatCompletionProps> = ({ completion, showAssistantMessage }) => {
    // Use a state to track open messages by their indices
    const [openIndices, setOpenIndices] = useState<number[]>([]);

    useEffect(() => {
        let initialIndices: number[] = [];

        if (showAssistantMessage) {
            // If showAssistantMessage is true, open the assistant messages by default
            initialIndices = completion.conversation
                .map((message, index) => message.role === 'assistant' ? index : -1)
                .filter(index => index !== -1);
        }

        setOpenIndices(initialIndices);
    }, [completion, showAssistantMessage]);


    return (
        <Box p={5} backgroundColor="white" shadow="md" borderWidth="1px" borderRadius="md" width="100%">
            <Text fontWeight="bold" fontSize="xs" color="gray.500" mb={4}>{completion.model}</Text>
            {completion.conversation.map((message, idx) => {
                let bgColor, textColor, btnColor, btnHoverColor;
                switch (message.role) {
                    case 'assistant':
                        bgColor = 'blue.100';
                        textColor = 'blue.600';
                        btnColor = 'blue.100';
                        btnHoverColor = 'blue.200';
                        break;
                    case 'system':
                        bgColor = 'red.100';
                        textColor = 'red.600';
                        btnColor = 'red.100';
                        btnHoverColor = 'red.200';
                        break;
                    default:
                        bgColor = 'gray.100';
                        textColor = 'black';
                        btnColor = 'gray.100';
                        btnHoverColor = 'gray.200';
                }
                const isOpen = openIndices.includes(idx);
                const label = message.name ? `${message.name} (${message.role}): ${message.content}` : `${message.role}: ${message.content}`;

                return (
                    <Box key={idx} mb={3}>
                        <Button
                            onClick={() => {
                                const newOpenIndices = isOpen
                                    ? openIndices.filter(index => index !== idx)
                                    : [...openIndices, idx];
                                setOpenIndices(newOpenIndices);
                            }}
                            variant="ghost"
                            width="full"
                            justifyContent="flex-start"
                            leftIcon={isOpen ? "▼" : "►"}
                            backgroundColor={btnColor}
                            color={textColor}
                            _hover={{ backgroundColor: btnHoverColor }}
                            textOverflow="ellipsis"
                            isTruncated
                            maxWidth="90%" // Adjust based on your preference
                        >
                            {isOpen ? label.split(":")[0] : label}
                        </Button>
                        <Collapse in={isOpen} startingHeight={0}>
                            <Box
                                p={3}
                                borderRadius="md"
                                bg={bgColor}
                            >
                                <Text
                                    fontWeight="medium"
                                    color={textColor}
                                    whiteSpace="pre-wrap"
                                >
                                    {message.content}
                                </Text>
                            </Box>
                        </Collapse>
                    </Box>
                );
            })}
        </Box>
    );
}

export default ChatCompletionComponent;
