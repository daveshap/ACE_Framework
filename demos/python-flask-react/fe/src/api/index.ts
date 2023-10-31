import { useState, useEffect } from "react"

export const getBusMessages = async (layerNum: number) => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/get_messages?layer=${layerNum}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })

  if (res.ok) {
    return res.text()
  }
}

type GenerateLlmMessageOptions = {
  onGeneration: () => void
  onSuccess: (message: string) => void
  enabled: boolean
}
export const useGenerateLlmMessage = (
  layerNum: number,
  { onGeneration, onSuccess, enabled }: GenerateLlmMessageOptions,
  messages?: string,
) => {
  const [llmMessage, setLlmMessage] = useState<string>("")
  const [done, setDone] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)

  useEffect(() => {
    const generateMessage = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat_completion`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          layer: layerNum,
          messages,
        }),
      })

      if (!res.body) return
      const decoder = new TextDecoderStream()
      const reader = res.body.pipeThrough(decoder).getReader()

      while (true) {
        let { value, done } = await reader.read()

        if (done) {
          setDone(true)
          break
        } else {
          setLlmMessage((message) => message + value)
        }
      }
    }

    const runSequence = async () => {
      setIsLoading(true)
      setLlmMessage("")
      onGeneration()
      await generateMessage()
      setIsLoading(false)
    }

    if (enabled) runSequence()
  }, [messages, layerNum, enabled])

  useEffect(() => {
    if (done) onSuccess(llmMessage)
  }, [done, llmMessage])

  return { llmMessage, isLoading, done }
}

export const saveResponse = async (layerNum: number, response: string) => {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/save_response`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      layer: layerNum,
      response,
    }),
  })

  if (res.ok) {
    return res.text()
  }
}
