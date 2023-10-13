"use client"

import { useAce } from "@/hooks/useAce"

// components
import { Button } from "./ui/button"

// icons
import { TriangleDownIcon, TriangleUpIcon } from "@radix-ui/react-icons"

const Message = ({ direction, layerNum }: { direction: string; layerNum: number }) => {
  const ace = useAce((state) => state)

  if (ace.layerStep === "BUS-MESSAGE") {
    if (
      (direction === "SOUTH" && ace.layerNum === layerNum + 1) ||
      (direction === "NORTH" && ace.layerNum === layerNum)
    ) {
      return "Fetching Bus..."
    }
  }

  if (ace.layerStep === "SAVE-RESPONSE") {
    if (
      (direction === "SOUTH" && ace.layerNum === layerNum) ||
      (direction === "NORTH" && ace.layerNum - 1 === layerNum)
    ) {
      return "Saving Response..."
    }
  }

  return `${direction[0] + direction.slice(1).toLocaleLowerCase()} Bus ${layerNum}`
}

const Arrows = ({ direction, layerNum, bound }: { direction: string; layerNum: number; bound: "UPPER" | "LOWER" }) => {
  const ace = useAce((state) => state)

  const getIsActivated = () => {
    if (!ace.started) return false
    // when retrieving bus messages
    if (ace.layerStep === "BUS-MESSAGE") {
      if (
        (bound === "UPPER" && direction === "NORTH" && ace.layerNum === layerNum) ||
        (bound === "LOWER" && direction === "SOUTH" && ace.layerNum - 1 === layerNum)
      ) {
        return true
      }
    }
    // when saving response
    if (ace.layerStep === "SAVE-RESPONSE") {
      if (
        (bound === "UPPER" && direction === "SOUTH" && layerNum === ace.layerNum) ||
        (bound === "LOWER" && direction === "NORTH" && layerNum === ace.layerNum - 1)
      ) {
        return true
      }
    }

    return false
  }

  if (direction.includes("NORTH")) {
    return [...Array(3).keys()].map((i) => (
      <TriangleUpIcon key={i} className={`h-12 w-12 fill-current ${getIsActivated() && "text-primary"}`} />
    ))
  } else {
    return [...Array(3).keys()].map((i) => (
      <TriangleDownIcon key={i} className={`h-12 w-12 fill-current  ${getIsActivated() && "text-primary"}`} />
    ))
  }
}

type BusProps = {
  layerNum: number
}
export default function Bus({ layerNum }: BusProps) {
  return (
    <div className="flex justify-center gap-x-24 px-24 py-4">
      {["SOUTH", "NORTH"].map((direction) => (
        <div className="flex flex-col items-center gap-y-4" key={direction}>
          <Arrows direction={direction} layerNum={layerNum} bound="UPPER" />
          <Button variant="outline" className="w-[175px]">
            <Message direction={direction} layerNum={layerNum} />
          </Button>
          <Arrows direction={direction} layerNum={layerNum} bound="LOWER" />
        </div>
      ))}
    </div>
  )
}
