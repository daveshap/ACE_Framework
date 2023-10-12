"use client"

import { ChangeEvent, useState, FormEvent } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { PaperPlaneIcon } from "@radix-ui/react-icons"

// components
import Spin from "@/components/ui/spin"

// utils
import { useChat } from "@/hooks/useChat"
import { useAce } from "@/hooks/useAce"

export default function Chat() {
  const { messages, addMessage } = useChat((state) => state)
  const ace = useAce((state) => state)
  const [inputValue, setInputValue] = useState("")
  const acePrint = { layer: ace.layerNum, bus: ace.bus, direction: ace.direction, step: ace.layerStep }

  console.log(JSON.stringify(acePrint))

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value)
  }

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (inputValue) {
      addMessage({ role: "user", text: inputValue })
      ace.startAce()
      setInputValue("")
    }
  }

  return (
    <form
      className="flex-grow relative max-h-[50vh] lg:max-w-[50vw] lg:max-h-full flex flex-col px-6 py-3 gap-3"
      onSubmit={onSubmit}
    >
      {/* Chat Messages */}
      {messages.map((message, i) => (
        <div
          className={`flex items-center rounded-lg min-w-[50px] max-w-[75%] text-sm py-3 px-4 whitespace-pre-wrap ${
            message.role === "user"
              ? "bg-primary text-primary-foreground self-start"
              : "bg-muted text-secondary-foreground self-end"
          }`}
          key={i}
        >
          {message.text}
        </div>
      ))}
      {ace.started && (
        <div className="relative flex items-center rounded-lg h-10 px-4 bg-muted text-secondary-foreground self-end">
          <Spin className="mx-auto" />
        </div>
      )}

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
