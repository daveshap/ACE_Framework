// pages/index.tsx
import {Box, Image, VStack} from '@chakra-ui/react';
import NextLink from 'next/link';
import React from "react";

const IndexPage = () => {
    return (
        <Box textAlign="center" fontSize="xl">
            <VStack spacing={8} py={20}>
                <Image src="/images/stacey-160.png" alt="Stacey" borderRadius="full"  mb={8} />
                <NextLink href="/chat" passHref>
                    Chat with Stacey
                </NextLink>
                <NextLink href="/admin" passHref>
                    Look inside Stacey's brain
                </NextLink>
            </VStack>
        </Box>
    );
};

export default IndexPage;
