'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { STACK } from '@/lib/data'

export default function StackSection() {
  const { ref, inView } = useInView()
  return (
    <section id="stack" className="py-24 px-6 md:px-12 bg-surface/40 border-y border-white/5">
      <div className="max-w-7xl mx-auto">
        <SectionTag label="Architecture" />
        <h2 className="font-syne text-3xl md:text-4xl font-extrabold tracking-tight mb-14">
          Engineering Stack
        </h2>
        <div
          ref={ref}
          className={`grid grid-cols-2 md:grid-cols-4 gap-px bg-white/5 border border-white/5 transition-all duration-700 ${inView ? 'opacity-100' : 'opacity-0'}`}
        >
          {STACK.map((s, i) => (
            <div key={i} className="bg-bg p-8">
              <div className="font-mono text-[10px] text-cyan uppercase tracking-[0.2em] mb-6 pb-3 border-b border-white/5">
                {s.layer}
              </div>
              <ul className="flex flex-col gap-1">
                {s.items.map((item, j) => (
                  <li
                    key={j}
                    className="font-mono text-[12px] text-text-mid py-[6px] border-b border-white/[0.03] hover:text-cyan transition-colors duration-150 cursor-default"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
