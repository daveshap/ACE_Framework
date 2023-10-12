import { create } from "zustand"
import { layers } from "@/lib/utils"

type State = {
  layerNum: keyof typeof layers
  layerStep: "BUS-MESSAGE" | "LLM-MESSAGE" | "SAVE-RESPONSE"
  bus: string[]
  type: "BUS" | "LAYER"
  direction: "NORTH" | "SOUTH"
  started: boolean
  auto: boolean
}
type AceState = State & {
  setAuto: (auto: boolean) => void
  startAce: () => void
  pivotAce: () => void
  stopAce: () => void
  progressAce: () => void
}
const initialState: State = {
  layerNum: 6,
  layerStep: "BUS-MESSAGE",
  bus: layers[6].bus,
  type: "LAYER",
  direction: "NORTH",
  started: false,
  auto: false,
}

export const useAce = create<AceState>((set) => ({
  ...initialState,
  setAuto: (auto) => set((state) => ({ ...state, auto })),
  startAce: () => set((state) => ({ ...state, started: true })),
  pivotAce: () =>
    set((state) => {
      // if the direction is going up and it's at the top layer, then pivot
      if (state.layerNum === 1 && state.direction === "NORTH") return { ...state, direction: "SOUTH" }

      return state
    }),
  stopAce: () =>
    set((state) => {
      // if the direction is going down and it's at the bottom layer, then it's done
      if (state.layerNum === 6 && state.direction === "SOUTH") return initialState

      return state
    }),
  progressAce: () =>
    set((state) => {
      // If a layer was just processed, then a bus needs to be processed next
      if (state.type === "LAYER" && state.layerStep === "BUS-MESSAGE") {
        return { ...state, layerStep: "LLM-MESSAGE" }
      } else if (state.type === "LAYER" && state.layerStep === "LLM-MESSAGE") {
        return { ...state, layerStep: "SAVE-RESPONSE", type: "BUS", bus: layers[state.layerNum].bus }
      } else if (state.type === "BUS" && state.direction === "NORTH") {
        return {
          ...state,
          layerNum: (state.layerNum - 1) as keyof typeof layers,
          type: "LAYER",
          layerStep: "BUS-MESSAGE",
        }
      } else {
        return {
          ...state,
          layerNum: (state.layerNum + 1) as keyof typeof layers,
          type: "LAYER",
          layerStep: "BUS-MESSAGE",
        }
      }
    }),
}))
