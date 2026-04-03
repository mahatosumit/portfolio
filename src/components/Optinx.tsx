'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { OPTINX_PILLARS, PROFILE } from '@/lib/data'
import { ArrowUpRight } from 'lucide-react'

export default function Optinx() {
  const { ref, inView } = useInView()
  return (
    <section
      id="optinx"
      className="py-24 px-6 md:px-12 bg-surface/30 border-y border-white/5"
    >
      <div className="max-w-7xl mx-auto">
        <SectionTag label="Venture" />
        <div
          ref={ref}
          className={`grid md:grid-cols-2 gap-16 md:gap-24 items-center transition-all duration-700 ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          {/* Left */}
          <div>
            <h2 className="font-syne text-5xl md:text-6xl font-extrabold text-cyan tracking-[-0.03em] mb-6">
              OPTINX
            </h2>
            <div className="flex flex-col gap-6">
              <p className="text-text-mid font-dm font-light text-[15px] leading-relaxed max-w-md">
                An AI and automation company building intelligent systems for real-world environments — across mobility, agriculture, and robotics.
              </p>
              
              <div className="flex items-center gap-6">
                <a
                  href={PROFILE.optinx}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-syne text-[11px] font-bold tracking-[0.2em] uppercase px-8 py-3 bg-cyan text-bg hover:bg-white transition-all duration-300 rounded-sm"
                >
                  Visit Website
                </a>
                
                <a
                  href={PROFILE.optinx}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-center gap-2 font-mono text-[11px] text-text-dim hover:text-cyan transition-colors duration-200"
                >
                  <span>{PROFILE.optinx.replace('https://', '').replace('/', '')}</span>
                  <ArrowUpRight size={14} className="group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform duration-300" />
                </a>
              </div>
            </div>
          </div>

          {/* Right — pillars */}
          <div className="border border-white/5">
            {OPTINX_PILLARS.map((pillar, i) => (
              <div
                key={i}
                className="flex items-center gap-4 px-7 py-5 border-b border-white/5 last:border-b-0 hover:bg-cyan/[0.03] transition-colors duration-200 group cursor-default"
              >
                <div className="w-[6px] h-[6px] rounded-full bg-cyan group-hover:scale-125 transition-transform duration-200 shrink-0" />
                <span className="font-syne font-semibold text-white text-[15px] tracking-tight">
                  {pillar}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
