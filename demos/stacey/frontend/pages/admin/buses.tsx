// pages/admin/Bus.tsx
import React from 'react';
import {Alert, HStack, Image, VStack} from '@chakra-ui/react';
import {Bus} from "@/components/bus";
import LayerStatus from "@/components/layerStatus";

const BusesPage = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    return (
        <HStack spacing={8} align="start">
            <Bus busName="northbound" />
            <VStack>
                <Image src="/images/stacey-160.png" alt="Stacey" borderRadius="full"  mb={8} />
                <LayerStatus />
            </VStack>
            <Bus busName="southbound" />
        </HStack>
    );
};

export default BusesPage;
