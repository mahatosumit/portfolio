'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { AWARDS, CERTIFICATIONS } from '@/lib/data'

export default function AwardsCerts() {
  const { ref, inView } = useInView()
  return (
    <section className="py-24 px-6 md:px-12 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <div
          ref={ref}
          className={`grid md:grid-cols-2 gap-16 transition-all duration-700 ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
        >
          {/* Awards */}
          <div>
            <SectionTag label="Recognition" />
            <h2 className="font-syne text-3xl font-extrabold tracking-tight mb-10">Awards</h2>
            <div className="flex flex-col border border-white/5">
              {AWARDS.map((a, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between px-7 py-5 border-b border-white/5 last:border-b-0 hover:bg-cyan/[0.02] transition-colors duration-200 group"
                >
                  <div>
                    <div className="font-syne font-bold text-cyan text-sm">{a.award}</div>
                    <div className="font-mono text-[11px] text-text-dim mt-0.5">{a.event}</div>
                  </div>
                  <div className="font-mono text-[10px] text-text-dim tracking-wider">{a.year}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Certifications */}
          <div>
            <SectionTag label="Credentials" />
            <h2 className="font-syne text-3xl font-extrabold tracking-tight mb-10">Certifications</h2>
            <ul className="flex flex-col gap-0 border border-white/5">
              {CERTIFICATIONS.map((cert, i) => (
                <li
                  key={i}
                  className="flex items-center gap-3 px-7 py-4 border-b border-white/5 last:border-b-0 hover:bg-cyan/[0.02] transition-colors duration-200 group"
                >
                  <span className="text-cyan text-[9px] shrink-0">▸</span>
                  <span className="font-mono text-[11px] text-text-dim group-hover:text-text-mid transition-colors duration-200">
                    {cert}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  )
}
