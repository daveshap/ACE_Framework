// pages/admin/Bus.tsx
import React from 'react';
import {Alert, HStack} from '@chakra-ui/react';
import {Bus} from "@/components/bus";

const BusesPage = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!backendUrl) {
        return <Alert status="error">I don't know where the backend is! Please set env variable NEXT_PUBLIC_BACKEND_URL</Alert>;
    }

    return (
        <HStack spacing={8}>
            <Bus busName="northbound" />
            <Bus busName="southbound" />
        </HStack>
    );
};

export default BusesPage;
