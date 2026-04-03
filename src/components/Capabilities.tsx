'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { CAPABILITIES } from '@/lib/data'

function CapCard({ num, title, arrow, desc, delay }: {
  num: string; title: string; arrow: string; desc: string; delay: number
}) {
  const { ref, inView } = useInView()
  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`group relative bg-bg border border-white/5 p-10 overflow-hidden transition-all duration-700 hover:bg-cyan/[0.02] hover:border-cyan/20 ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
    >
      {/* Left accent */}
      <div className="absolute left-0 top-0 w-[3px] h-0 bg-cyan group-hover:h-full transition-all duration-500" />

      <div className="font-mono text-[10px] text-text-dim tracking-[0.2em] mb-6">{num}</div>
      <h3 className="font-syne text-xl font-bold text-white mb-3 tracking-tight">{title}</h3>
      <p className="font-mono text-[11px] text-cyan mb-4">→ {arrow}</p>
      <p className="text-text-dim text-sm leading-relaxed">{desc}</p>
    </div>
  )
}

export default function Capabilities() {
  return (
    <section id="build" className="py-24 px-6 md:px-12 max-w-7xl mx-auto">
      <SectionTag label="Capabilities" />
      <h2 className="font-syne text-3xl md:text-4xl font-extrabold tracking-tight mb-14">
        What I Build
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-white/5 border border-white/5">
        {CAPABILITIES.map((c, i) => (
          <CapCard key={i} {...c} delay={i * 100} />
        ))}
      </div>
    </section>
  )
}
