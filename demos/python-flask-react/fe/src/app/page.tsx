"use client"

import { ChangeEvent, useState, FormEvent } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { PaperPlaneIcon } from "@radix-ui/react-icons"

// components
import Spin from "@/components/ui/spin"

type Message = {
  role: "assistant" | "user"
  text: string
  isLoading?: boolean
}
function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value)
  }

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (inputValue) {
      setMessages([...messages, { role: "user", text: inputValue }, { role: "assistant", text: "", isLoading: true }])
      setInputValue("")
    }
  }

  return (
    <form
      className="flex-grow relative max-h-1/2 lg:max-w-1/2 lg:max-h-full flex flex-col px-6 py-3 gap-3"
      onSubmit={onSubmit}
    >
      {/* Chat Messages */}
      {messages.map((message, i) => (
        <div
          className={`relative flex items-center rounded-lg min-w-[50px] max-w-[75%] text-sm h-10 px-4 ${
            message.role === "user"
              ? "bg-primary text-primary-foreground self-start"
              : "bg-muted text-secondary-foreground self-end"
          }`}
          key={i}
        >
          {message.isLoading ? <Spin className="mx-auto" /> : message.text}
        </div>
      ))}

      <div className="fixed left-0 bottom-0 w-full lg:w-1/2 px-6 py-3">
        {/* Message Box */}
        <div className="relative w-full h-full">
          <Input placeholder="send a message" className="w-full h-12" value={inputValue} onChange={handleInputChange} />
          <div className="absolute right-2 inset-y-0 flex items-center">
            <Button type="submit" size="icon" className="h-8 w-8">
              <PaperPlaneIcon />
            </Button>
          </div>
        </div>
      </div>
    </form>
  )
}

function Ace() {
  return (
    <section className="flex-grow max-h-1/2 lg:max-w-1/2 lg:max-h-full flex order-first lg:order-last border-b-2 border-b-gray-500 lg:border-b-0 lg:border-l-2 lg:border-l-gray-500 gap-y-12">
      <div></div>
    </section>
  )
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col lg:flex-row bg-gray-900">
      <Chat />
      <Ace />
    </main>
  )
}
