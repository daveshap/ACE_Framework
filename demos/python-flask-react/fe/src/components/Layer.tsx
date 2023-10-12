"use client"

import { useState } from "react"
import { useQuery } from "react-query"

// components
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

// api
import { getBusMessages, useGenerateLlmMessage, saveResponse } from "@/api"

// utils
import { layers, sleep } from "@/lib/utils"
import { useAce } from "@/hooks/useAce"
import { useChat, type Message } from "@/hooks/useChat"

const getMessages = (chatMessages: Message[], layerNum: number, direction: "NORTH" | "SOUTH", busMessages?: string) => {
  if (!busMessages) return ""
  const userMessage = chatMessages.find((message) => message.role === "user")
  if (userMessage && layerNum === 6 && direction === "NORTH") {
    return `USER message:\n${userMessage.text}\n\n${busMessages}`
  }

  return busMessages
}

type LayerProps = {
  layerNum: keyof typeof layers
}
export default function Layer({ layerNum }: LayerProps) {
  const [value, setValue] = useState("")
  const ace = useAce((state) => state)
  const chat = useChat((state) => state)

  const busMessages = useQuery(["get-bus-message", layerNum], () => getBusMessages(layerNum), {
    enabled: ace.started && ace.layerNum === layerNum && ace.type === "LAYER" && ace.layerStep === "BUS-MESSAGE",
    onSuccess: () => {
      setValue(`layer-${layerNum}-bus-message`)
      if (ace.auto) ace.progressAce()
    },
  })
  const messages = getMessages(chat.messages, ace.layerNum, ace.direction, busMessages.data)

  const llmMessage = useGenerateLlmMessage(
    layerNum,
    {
      enabled:
        ace.started &&
        ace.layerNum === layerNum &&
        ace.type === "LAYER" &&
        ace.layerStep === "LLM-MESSAGE" &&
        !!messages,
      onGeneration: () => setValue(`layer-${layerNum}-llm-message`),
      onSuccess: (llmMessage) => {
        // if it's at the bottom and it's going down, stop
        if (ace.layerNum === 6 && ace.direction === "SOUTH") {
          ace.stopAce()
          chat.addMessage({ role: "assistant", text: llmMessage })
        }
        if (ace.auto) ace.progressAce()
      },
    },
    messages,
  )

  useQuery(["save-response", layerNum, llmMessage.llmMessage], () => saveResponse(layerNum, llmMessage.llmMessage!), {
    enabled:
      ace.started &&
      ace.layerNum === layerNum &&
      ace.layerStep === "SAVE-RESPONSE" &&
      ace.type === "BUS" &&
      llmMessage.done,
    onSuccess: async () => {
      setValue("")
      // if it's at the top and it's going up, pivot
      if (ace.layerNum === 1 && ace.direction === "NORTH") ace.pivotAce()
      if (ace.auto) ace.progressAce()
    },
  })

  return (
    <div className="self-center w-1/2 flex flex-col gap-y-2 border border-zinc-800 px-8 py-6 rounded-md bg-zinc-800/20">
      <h1 className="text-center font-bold text-lg lg:text-xl">{layers[layerNum].name}</h1>

      <Accordion
        className={`${
          ace.started && ace.layerNum === layerNum ? "h-full block" : "h-0 opacity-0 hidden"
        } transition-all`}
        type="single"
        value={value}
        collapsible
      >
        <AccordionItem value={`layer-${layerNum}-bus-message`}>
          <AccordionTrigger isLoading={busMessages.isLoading}>Bus Messages Received</AccordionTrigger>
          <AccordionContent className="whitespace-pre-wrap">{messages}</AccordionContent>
        </AccordionItem>
        <AccordionItem value={`layer-${layerNum}-llm-message`}>
          <AccordionTrigger isLoading={llmMessage.isLoading}>LLM Message Generated</AccordionTrigger>
          <AccordionContent className="whitespace-pre-wrap">{llmMessage.llmMessage}</AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  )
}
