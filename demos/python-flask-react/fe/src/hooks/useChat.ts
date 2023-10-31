import { create } from "zustand"

export type Message = {
  role: "assistant" | "user"
  text: string
}
interface ChatState {
  messages: Message[]
  addMessage: (message: Message) => void
}

export const useChat = create<ChatState>((set) => ({
  messages: [],
  addMessage: (message: Message) => set((state) => ({ ...state, messages: [...state.messages, message] })),
}))
