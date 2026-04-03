'use client'
import { useInView } from '@/lib/useInView'
import { METRICS } from '@/lib/data'

function MetricItem({ value, label, delay }: { value: string; label: string; delay: number }) {
  const { ref, inView } = useInView(0.3)
  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`px-8 py-10 border-r border-white/5 last:border-r-0 transition-all duration-700 ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}
    >
      <div className="font-syne font-extrabold text-cyan leading-none tracking-tight mb-3 whitespace-pre-line"
        style={{ fontSize: value.includes('\n') ? '2rem' : '3.2rem' }}>
        {value}
      </div>
      <div className="font-mono text-[11px] text-text-dim uppercase tracking-[0.12em] leading-relaxed whitespace-pre-line">
        {label}
      </div>
    </div>
  )
}

export default function Metrics() {
  return (
    <div className="border-y border-white/5 grid grid-cols-2 md:grid-cols-4 max-w-7xl mx-auto w-full">
      {METRICS.map((m, i) => (
        <MetricItem key={i} value={m.value} label={m.label} delay={i * 120} />
      ))}
    </div>
  )
}
