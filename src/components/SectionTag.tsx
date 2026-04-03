export default function SectionTag({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-3 mb-5">
      <span className="font-mono text-[10px] text-cyan tracking-[0.25em] uppercase">{label}</span>
      <span className="w-12 h-px bg-cyan/30" />
    </div>
  )
}
