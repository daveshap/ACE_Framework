"use client"

import { ThickArrowDownIcon, ThickArrowUpIcon } from "@radix-ui/react-icons"
import { useAce } from "@/hooks/useAce"

// components
import { Button } from "./ui/button"
import Spin from "./ui/spin"

const Icon = ({ busType }: { busType: string }) => {
  const ace = useAce((state) => state)
  if (ace.type === "BUS" && ace.bus.includes(busType)) return <Spin className="w-4 h-4" />
  if (busType.includes("SOUTH")) return <ThickArrowDownIcon className="w-[50px] h-[50px]" />
  if (busType.includes("NORTH")) return <ThickArrowUpIcon className="w-[50px] h-[50px]" />
}

type BusProps = {
  bus: string[]
}
export default function Bus({ bus }: BusProps) {
  return (
    <div className="flex justify-between px-24">
      {bus.map((busType) => (
        <Button variant="outline" size="icon" className="w-[60px] h-[60px]" key={busType}>
          <Icon busType={busType} />
        </Button>
      ))}
    </div>
  )
}
