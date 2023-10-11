"use client"

import { QueryClient, QueryClientProvider } from "react-query"

// Create a client
const queryClient = new QueryClient()

export default function Providers({ children }: { children: React.ReactNode }) {
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
