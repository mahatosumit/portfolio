'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { MINDSET } from '@/lib/data'

export default function MindsetSection() {
  const { ref, inView } = useInView()
  return (
    <section className="py-24 px-6 md:px-12 bg-surface/20 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <SectionTag label="Engineering Mindset" />
        <div
          ref={ref}
          className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 mt-14 transition-all duration-700 ${inView ? 'opacity-100' : 'opacity-0'}`}
        >
          {MINDSET.map((m, i) => (
            <div
              key={i}
              className="group pt-6 border-t-2 border-white/5 hover:border-cyan transition-colors duration-300"
              style={{ transitionDelay: `${i * 80}ms` }}
            >
              <p className="font-syne font-bold text-white text-[1.05rem] leading-snug tracking-tight group-hover:text-cyan transition-colors duration-300">
                {m}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
