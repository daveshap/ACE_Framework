import { create } from "zustand"
import { layers } from "@/lib/utils"

type State = {
  layerNum: keyof typeof layers
  bus: string[]
  type: "BUS" | "LAYER"
  direction: "UP" | "DOWN"
  started: boolean
}
type AceState = State & {
  startAce: () => void
  pivotAce: () => void
  stopAce: () => void
  progressAce: () => void
}
const initialState: State = {
  layerNum: 6,
  bus: layers[6].bus,
  type: "LAYER",
  direction: "UP",
  started: false,
}

export const useAce = create<AceState>((set) => ({
  ...initialState,
  startAce: () => set((state) => ({ ...state, started: true })),
  pivotAce: () =>
    set((state) => {
      // if the direction is going up and it's at the top layer, then pivot
      if (state.layerNum === 1 && state.direction === "UP") return { ...state, direction: "DOWN" }

      return state
    }),
  stopAce: () =>
    set((state) => {
      // if the direction is going down and it's at the bottom layer, then it's done
      if (state.layerNum === 6 && state.direction === "DOWN") return initialState

      return state
    }),
  progressAce: () =>
    set((state) => {
      // If a layer was just processed, then a bus needs to be processed next
      if (state.type === "LAYER") {
        return { ...state, bus: layers[state.layerNum].bus, type: "BUS" }
      } else if (state.type === "BUS" && state.direction === "UP") {
        return { ...state, layerNum: (state.layerNum - 1) as keyof typeof layers, type: "LAYER" }
      } else {
        return { ...state, layerNum: (state.layerNum + 1) as keyof typeof layers, type: "LAYER" }
      }
    }),
}))
