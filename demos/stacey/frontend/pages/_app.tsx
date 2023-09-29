import type { AppProps } from 'next/app'
import React from "react";
import { ChakraProvider } from "@chakra-ui/react";

export default function App({ Component, pageProps }: AppProps) {
  return (
      <ChakraProvider>
        <Component {...pageProps} />
      </ChakraProvider>
  )
}
