'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'

const links = [
  { href: '#build', label: 'Build' },
  { href: '#delivered', label: 'Delivered' },
  { href: '#stack', label: 'Stack' },
  { href: '#projects', label: 'Projects' },
  { href: '#optinx', label: 'OPTINX' },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled ? 'bg-bg/90 backdrop-blur-md border-b border-white/5' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-12 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="font-mono text-xs text-cyan tracking-[0.2em] uppercase">
          SM <span className="text-white/20 mx-1">{'//'}</span> Systems Engineer
        </div>

        {/* Links */}
        <ul className="hidden md:flex items-center gap-8">
          {links.map((l) => (
            <li key={l.href}>
              <a
                href={l.href}
                className="font-mono text-[11px] text-text-dim hover:text-cyan tracking-[0.12em] uppercase transition-colors duration-200"
              >
                {l.label}
              </a>
            </li>
          ))}
        </ul>

        {/* CTA */}
        <a
          href="mailto:sumitmahato0913@gmail.com"
          className="hidden md:block font-syne text-xs font-bold tracking-widest uppercase px-5 py-2 border border-cyan/30 text-cyan hover:bg-cyan hover:text-black transition-all duration-200"
        >
          Contact
        </a>
      </div>
    </nav>
  )
}
