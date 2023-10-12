"use client"

import { TriangleRightIcon } from "@radix-ui/react-icons"

// components
import Bus from "@/components/Bus"
import Layer from "@/components/Layer"
import { Button } from "./ui/button"

// hooks
import { useAce } from "@/hooks/useAce"

const getBus = (layerNum: number) => ["SOUTH", "NORTH"].map((bus) => `${bus}-${layerNum}`)

export default function Ace() {
  const ace = useAce((state) => state)

  const next = () => {
    if (!ace.auto && ace.started) ace.progressAce()
  }

  return (
    <section className="relative flex-grow flex flex-col py-6 max-h-[50vh] lg:max-w-[50vw] lg:max-h-full order-first lg:order-last border-b-2 border-b-gray-500 lg:border-b-0 lg:border-l-2 lg:border-l-gray-500 overflow-y-scroll">
      <Button variant="default" size="icon" className="fixed top-0 right-0 m-4" onClick={() => next()}>
        <TriangleRightIcon className="h-8 w-8" />
      </Button>

      <Layer layerNum={1} />
      <Bus bus={getBus(1)} />
      <Layer layerNum={2} />
      <Bus bus={getBus(2)} />
      <Layer layerNum={3} />
      <Bus bus={getBus(3)} />
      <Layer layerNum={4} />
      <Bus bus={getBus(4)} />
      <Layer layerNum={5} />
      <Bus bus={getBus(5)} />
      <Layer layerNum={6} />
    </section>
  )
}
