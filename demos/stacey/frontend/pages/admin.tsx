// pages/admin/Bus.tsx
import React, {useRef} from 'react';
import {Alert, Box, Heading, HStack, Image, VStack} from '@chakra-ui/react';
import {Bus} from "@/components/bus";
import LayerStatus from "@/components/layerStatus";
import {WebSocketProvider} from "@/context/WebSocketContext";

const BusesPage = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const socketRef = useRef<WebSocket | null>(null);


    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    /*
    useEffect(() => {
        if (!backendUrl) {
            console.error("NEXT_PUBLIC_BACKEND_URL is not set");
            return;
        }

        socketRef.current = new WebSocket(`ws://localhost:5000/ws/`);
        console.log("Got socket:" + socketRef.current);

        socketRef.current.onmessage = (event) => {
            console.log("Admin onmessage", event.data);
        };

        return () => {
            console.log("Closing socket")
            socketRef.current?.close();
        };
    }, [backendUrl]);

     */

    return (
        <WebSocketProvider>

            <Box backgroundColor="black" minH="100vh">
                <VStack w={"full"}>
                    <Heading color={"white"} >Stacey's brain</Heading>
                    <HStack spacing={8} align="start">
                        <Bus busName="southbound" />
                        <VStack>
                            <Image src="/images/stacey-160.png" alt="Stacey" borderRadius="full"  mb={8} />
                            <LayerStatus layerId={1} displayName={"Layer 1: Aspirational 🌟"} backgroundColor={"red.100"} />
                            <LayerStatus layerId={2} displayName={"Layer 2: Global Strategy 🌐"} backgroundColor={"orange.100"} />
                            <LayerStatus layerId={3} displayName={"Layer 3: Agent Model 🤖"} backgroundColor={"yellow.100"} />
                            <LayerStatus layerId={4} displayName={"Layer 4: Executive Function 🧠"} backgroundColor={"green.100"} />
                            <LayerStatus layerId={5} displayName={"Layer 5: Cognitive Control ⚙️"} backgroundColor={"teal.100"} />
                            <LayerStatus layerId={6} displayName={"Layer 6: Task Prosecution 🛠️"} backgroundColor={"blue.100"} />
                        </VStack>
                        <Bus busName="northbound" />
                    </HStack>
                </VStack>
            </Box>
        </WebSocketProvider>
    );
};

export default BusesPage;
