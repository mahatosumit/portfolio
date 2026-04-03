'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { NEXT_BUILDS } from '@/lib/data'

const statusColor: Record<string, string> = {
  Active: 'text-cyan',
  Building: 'text-green-400',
  Research: 'text-yellow-400',
  Expanding: 'text-violet-400',
}

export default function NextBuilds() {
  const { ref, inView } = useInView()
  return (
    <section className="py-24 px-6 md:px-12 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <SectionTag label="In Progress" />
        <h2 className="font-syne text-3xl md:text-4xl font-extrabold tracking-tight mb-14">
          What I&apos;m Building Next
        </h2>
        <div
          ref={ref}
          className={`flex flex-col max-w-2xl transition-all duration-700 ${inView ? 'opacity-100' : 'opacity-0'}`}
        >
          {NEXT_BUILDS.map((item, i) => (
            <div
              key={i}
              className="flex items-baseline gap-6 py-6 border-b border-white/5 last:border-b-0 group"
              style={{ transitionDelay: `${i * 80}ms` }}
            >
              <div className="font-syne font-bold text-white text-base w-44 shrink-0 group-hover:text-cyan transition-colors duration-200">
                {item.name}
              </div>
              <div className="font-mono text-[12px] text-text-dim flex-1">{item.desc}</div>
              <div className={`font-mono text-[10px] uppercase tracking-[0.15em] whitespace-nowrap flex items-center gap-1.5 ${statusColor[item.status] ?? 'text-text-dim'}`}>
                <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
                {item.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
