'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { EXPERIENCE } from '@/lib/data'

function ExpRow({ org, role, period, problem, system, impact, delay }: {
  org: string; role: string; period: string; problem: string; system: string; impact: string; delay: number
}) {
  const { ref, inView } = useInView()
  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`group grid md:grid-cols-[200px_1fr_1fr] gap-6 md:gap-12 p-8 md:p-10 border-b border-white/5 last:border-b-0 hover:bg-cyan/[0.02] transition-all duration-500 relative ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
    >
      {/* Side accent */}
      <div className="absolute left-0 top-0 w-[2px] h-0 bg-cyan group-hover:h-full transition-all duration-500" />

      <div>
        <div className="font-mono text-xs text-cyan font-medium tracking-wider mb-1">{org}</div>
        <div className="font-syne font-bold text-white text-[15px] leading-snug">{role}</div>
        <div className="font-mono text-[10px] text-text-dim mt-1 tracking-wide">{period}</div>
      </div>

      <div>
        <div className="font-mono text-[10px] text-text-dim uppercase tracking-[0.15em] mb-2">System Built</div>
        <p className="text-text-mid text-sm leading-relaxed">{system}</p>
      </div>

      <div>
        <div className="font-mono text-[10px] text-text-dim uppercase tracking-[0.15em] mb-2">Impact</div>
        <p className="font-mono text-[12px] text-cyan/70 leading-relaxed">{impact}</p>
      </div>
    </div>
  )
}

export default function Experience() {
  return (
    <section id="delivered" className="py-0 pb-24 px-6 md:px-12 max-w-7xl mx-auto">
      <SectionTag label="Proof of Work" />
      <h2 className="font-syne text-3xl md:text-4xl font-extrabold tracking-tight mb-14">
        Systems Delivered in Real Environments
      </h2>
      <div className="border border-white/5">
        {EXPERIENCE.map((e, i) => (
          <ExpRow key={i} {...e} delay={i * 100} />
        ))}
      </div>
    </section>
  )
}
