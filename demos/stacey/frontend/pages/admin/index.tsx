// pages/watch/index.tsx
import {Heading, VStack} from '@chakra-ui/react';
import React from "react";
import BusLogs from "@/pages/admin/busLogs";

const IndexPage = () => {
    return (
        <VStack>
            <Heading>Stacey's brain</Heading>
            <BusLogs></BusLogs>
        </VStack>
    );
};

export default IndexPage;
