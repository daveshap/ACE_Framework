// pages/watch/index.tsx
import {Heading, VStack} from '@chakra-ui/react';
import React from "react";
import Buses from "@/pages/admin/buses";

const IndexPage = () => {
    return (
        <VStack w={"full"}>
            <Heading>Stacey's brain</Heading>
            <Buses></Buses>
        </VStack>
    );
};

export default IndexPage;
