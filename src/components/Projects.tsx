'use client'
import { useInView } from '@/lib/useInView'
import SectionTag from './SectionTag'
import { PROJECTS } from '@/lib/data'
import { ExternalLink } from 'lucide-react'

function Pipeline({ steps }: { steps: string[] }) {
  return (
    <div className="flex flex-wrap items-center gap-1 mb-5">
      {steps.map((step, i) => (
        <span key={i} className="flex items-center gap-1">
          <span className="font-mono text-[10px] text-text-dim bg-white/[0.04] px-2 py-[3px]">
            {step}
          </span>
          {i < steps.length - 1 && (
            <span className="font-mono text-[10px] text-cyan">→</span>
          )}
        </span>
      ))}
    </div>
  )
}

function ProjectCard({ num, name, role, pipeline, tech, impact, github, delay }: {
  num: string; name: string; role: string; pipeline: string[]
  tech: string[]; impact: string; github: string; delay: number
}) {
  const { ref, inView } = useInView()
  return (
    <div
      ref={ref}
      style={{ transitionDelay: `${delay}ms` }}
      className={`group relative bg-bg p-9 overflow-hidden hover:bg-cyan/[0.015] transition-all duration-500 ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'}`}
    >
      {/* Top accent line */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-white/5 group-hover:bg-cyan/30 transition-colors duration-500" />

      <div className="font-mono text-[10px] text-text-dim tracking-[0.2em] mb-4">PROJECT {num}</div>

      <div className="flex items-start justify-between mb-1">
        <h3 className="font-syne text-xl font-extrabold text-white tracking-tight">{name}</h3>
        {github && (
          <a
            href={github}
            target="_blank"
            rel="noopener noreferrer"
            className="text-text-dim hover:text-cyan transition-colors ml-3 mt-1"
          >
            <ExternalLink size={14} />
          </a>
        )}
      </div>

      <div className="font-mono text-[11px] text-cyan mb-6">{role}</div>

      <Pipeline steps={pipeline} />

      <div className="flex flex-wrap gap-[6px] mb-5">
        {tech.map((t, i) => (
          <span
            key={i}
            className="font-mono text-[10px] px-2 py-[3px] border border-white/5 text-text-dim group-hover:border-cyan/15 group-hover:text-text-mid transition-all duration-300"
          >
            {t}
          </span>
        ))}
      </div>

      <p className="font-mono text-[12px] text-cyan/60">{impact}</p>
    </div>
  )
}

export default function Projects() {
  return (
    <section id="projects" className="py-24 px-6 md:px-12 max-w-7xl mx-auto">
      <SectionTag label="Systems Engineered" />
      <h2 className="font-syne text-3xl md:text-4xl font-extrabold tracking-tight mb-14">
        Projects Built
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-white/5 border border-white/5">
        {PROJECTS.map((p, i) => (
          <ProjectCard key={i} {...p} delay={i * 80} />
        ))}
      </div>
    </section>
  )
}
