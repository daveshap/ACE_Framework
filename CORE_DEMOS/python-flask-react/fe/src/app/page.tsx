import Ace from "@/components/Ace"
import Chat from "@/components/Chat"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col lg:flex-row bg-gray-950">
      <Chat />
      <Ace />
    </main>
  )
}
