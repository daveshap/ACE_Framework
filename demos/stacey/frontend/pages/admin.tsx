// pages/admin/Bus.tsx
import React from 'react';
import {Alert, Box, Flex, Heading, Image, VStack} from '@chakra-ui/react';
import {Bus} from "@/components/bus";
import LayerStatus from "@/components/layerStatus";
import {WebSocketProvider} from "@/context/WebSocketContext";

const AdminPage = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    return (
        <WebSocketProvider>

            <Box backgroundColor="black" minH="100vh">
                <VStack w={"full"}>
                    <Heading color={"white"} >Stacey's brain</Heading>
                    <Flex w="full" align="start">
                        <Box flex="1" mx="3"><Bus busName="southbound" /></Box>
                        <VStack>
                            <Image src="/images/stacey-160.png" alt="Stacey" borderRadius="full"  mb={8} />
                            <LayerStatus layerId={1} displayName={"Layer 1: Aspirational 🌟"} backgroundColor={"red.100"} />
                            <LayerStatus layerId={2} displayName={"Layer 2: Global Strategy 🌐"} backgroundColor={"orange.100"} />
                            <LayerStatus layerId={3} displayName={"Layer 3: Agent Model 🤖"} backgroundColor={"yellow.100"} />
                            <LayerStatus layerId={4} displayName={"Layer 4: Executive Function 🧠"} backgroundColor={"green.100"} />
                            <LayerStatus layerId={5} displayName={"Layer 5: Cognitive Control ⚙️"} backgroundColor={"teal.100"} />
                            <LayerStatus layerId={6} displayName={"Layer 6: Task Prosecution 🛠️"} backgroundColor={"blue.100"} />
                        </VStack>
                        <Box flex="1" mx="3"><Bus busName="northbound" /></Box>
                    </Flex>
                </VStack>
            </Box>
        </WebSocketProvider>
    );
};

export default AdminPage;
