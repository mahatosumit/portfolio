'use client'
import dynamic from 'next/dynamic'
import { PROFILE, PROOF_STRIP } from '@/lib/data'

const SystemCanvas = dynamic(() => import('./SystemCanvas'), { ssr: false })

export default function Hero() {
  return (
    <section className="relative min-h-screen grid md:grid-cols-2 items-center gap-12 px-6 md:px-12 pt-24 pb-16 max-w-7xl mx-auto">
      {/* Ambient glow */}
      <div className="absolute -bottom-40 -left-40 w-[500px] h-[500px] rounded-full bg-cyan/5 blur-[120px] pointer-events-none" />

      {/* LEFT */}
      <div className="relative z-10">
        {/* Tag */}
        <div className="flex items-center gap-3 mb-8">
          <span className="w-5 h-px bg-cyan" />
          <span className="font-mono text-[11px] text-cyan tracking-[0.2em] uppercase">
            Autonomous Systems Engineer
          </span>
        </div>

        {/* Headline */}
        <h1 className="font-syne text-4xl md:text-5xl lg:text-[3.5rem] font-extrabold leading-[1.05] tracking-[-0.02em] mb-7">
          I Build Systems That{' '}
          <span className="text-gradient">See, Think,</span>
          <br />
          and Drive Themselves
        </h1>

        <p className="text-text-mid font-dm font-light text-base leading-relaxed max-w-md mb-10">
          {PROFILE.subtext}
        </p>

        {/* Proof strip */}
        <ul className="flex flex-col gap-[10px] mb-10">
          {PROOF_STRIP.map((p, i) => (
            <li key={i} className="flex items-baseline gap-3 font-mono text-[11px]">
              <span className="text-cyan text-[10px] shrink-0">▸</span>
              <span className="text-text-dim">
                <span className="text-text-mid font-medium">{p.label}</span>
                {p.detail && (
                  <span className="text-text-dim"> — {p.detail}</span>
                )}
              </span>
            </li>
          ))}
        </ul>

        {/* CTAs */}
        <div className="flex flex-wrap gap-4">
          <a
            href="#projects"
            className="font-syne text-[13px] font-bold tracking-widest uppercase px-7 py-3 bg-cyan text-black hover:bg-white transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(0,255,180,0.3)]"
          >
            Explore Systems
          </a>
          <a
            href={`mailto:${PROFILE.email}`}
            className="font-syne text-[13px] font-bold tracking-widest uppercase px-7 py-3 border border-cyan/30 text-cyan hover:bg-cyan/10 hover:border-cyan transition-all duration-200 hover:-translate-y-0.5"
          >
            Work With Me
          </a>
        </div>
      </div>

      {/* RIGHT — Animated Canvas */}
      <div className="hidden md:block relative w-full aspect-square max-w-[520px] ml-auto">
        <SystemCanvas />
      </div>
    </section>
  )
}
