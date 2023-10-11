// components
import Bus from "@/components/Bus"
import Layer from "@/components/Layer"

const getBus = (layerNum: number) => ["SOUTH", "NORTH"].map((bus) => `${bus}-${layerNum}`)

export default function Ace() {
  return (
    <section className="flex-grow flex flex-col gap-y-6 py-6 max-h-[50vh] lg:max-w-[50vw] lg:max-h-full order-first lg:order-last border-b-2 border-b-gray-500 lg:border-b-0 lg:border-l-2 lg:border-l-gray-500 overflow-y-scroll">
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
