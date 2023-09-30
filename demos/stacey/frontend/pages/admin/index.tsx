// pages/watch/index.tsx
import {Heading, VStack} from '@chakra-ui/react';
import React from "react";
import Bus from "@/pages/admin/bus";

const IndexPage = () => {
    return (
        <VStack>
            <Heading>Stacey's brain</Heading>
            <Bus></Bus>
        </VStack>
    );
};

export default IndexPage;
