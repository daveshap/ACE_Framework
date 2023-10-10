import { twMerge } from "tailwind-merge"

function Pulse({ className }: { className?: string }) {
  return (
    <span className={twMerge("relative flex h-3 w-3", className)}>
      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary/90 opacity-75"></span>
      <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
    </span>
  )
}

export default Pulse
