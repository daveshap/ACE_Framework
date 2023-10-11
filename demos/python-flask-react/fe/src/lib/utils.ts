import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const layers = {
  1: {
    name: "Aspirational Layer",
    bus: ["SOUTH-1"],
  },
  2: {
    name: "Global Strategy",
    bus: ["NORTH-1", "SOUTH-2"],
  },
  3: {
    name: "Agent Model",
    bus: ["NORTH-2", "SOUTH-3"],
  },
  4: {
    name: "Executive Function",
    bus: ["NORTH-3", "SOUTH-4"],
  },
  5: {
    name: "Cognitive Control",
    bus: ["NORTH-4", "SOUTH-5"],
  },
  6: {
    name: "Task Prosecution",
    bus: ["NORTH-5"],
  },
}

export const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))
