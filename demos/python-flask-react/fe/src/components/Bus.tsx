"use client"

import { useAce } from "@/hooks/useAce"

// components
import { Button } from "./ui/button"

// icons
import { TriangleDownIcon, TriangleUpIcon } from "@radix-ui/react-icons"

const Message = ({ busType }: { busType: string }) => {
  const ace = useAce((state) => state)
  const [direction, layerNum] = busType.split("-")
  if (ace.type === "BUS" && ace.bus.includes(busType)) return "Saving Response to bus..."

  return `${direction[0] + direction.slice(1).toLocaleLowerCase()} Bus ${layerNum}`
}

const Arrows = ({ busType }: { busType: string }) => {
  const ace = useAce((state) => state)
  const [direction, layerNum] = busType.split("-")

  const getIsActivated = () => {
    // it's activated if it's saving the response
    if (ace.type === "BUS" && ace.bus.includes(busType)) return true
    // it's activated if it's retrieving the bus messages
    if (ace.type === "LAYER" && ace.layerStep === "BUS-MESSAGE") {
      if (direction === "NORTH" && Number(layerNum) === ace.layerNum + 1) return true
      if (direction === "SOUTH" && Number(layerNum) === ace.layerNum - 1) return true
    }

    return false
  }

  if (busType.includes("NORTH")) {
    return [...Array(3).keys()].map((i) => (
      <TriangleUpIcon key={i} className={`h-12 w-12 ${getIsActivated() && "fill-primary"}`} />
    ))
  } else {
    return [...Array(3).keys()].map((i) => (
      <TriangleDownIcon key={i} className={`h-12 w-12 ${getIsActivated() && "fill-primary"}`} />
    ))
  }
}

type BusProps = {
  bus: string[]
}
export default function Bus({ bus }: BusProps) {
  return (
    <div className="flex justify-center gap-x-24 px-24 py-4">
      {bus.map((busType) => (
        <div className="flex flex-col items-center gap-y-4" key={busType}>
          <Arrows busType={busType} />
          <Button variant="outline">
            <Message busType={busType} />
          </Button>
          <Arrows busType={busType} />
        </div>
      ))}
    </div>
  )
}
