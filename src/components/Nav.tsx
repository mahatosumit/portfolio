'use client'
import { useState, useEffect } from 'react'
import { Menu, X } from 'lucide-react'
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
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled || isOpen ? 'bg-bg/95 backdrop-blur-md border-b border-white/5' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-12 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="font-syne text-sm md:text-base font-bold text-cyan tracking-[0.15em] uppercase">
            SUMIT MAHATO
          </div>
          <div className="hidden sm:flex items-center gap-3">
            <span className="text-white/10 h-4 w-[1px] bg-white/10" />
            <span className="font-syne text-sm md:text-base font-bold text-cyan tracking-[0.15em] uppercase">
              Systems Engineer
            </span>
          </div>
        </div>

        {/* Links */}
        <ul className="hidden md:flex items-center gap-8">
          {links.map((l) => (
            <li key={l.href}>
              <a
                href={l.href}
                className="font-syne text-[12px] md:text-[13px] text-text-dim hover:text-cyan tracking-[0.15em] uppercase transition-all duration-300 hover:tracking-[0.2em]"
              >
                {l.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Desktop CTA */}
        <a
          href="mailto:sumitmahato0913@gmail.com"
          className="hidden md:block font-syne text-[11px] font-bold tracking-[0.2em] uppercase px-6 py-2.5 border border-cyan/20 text-cyan hover:bg-cyan hover:text-bg hover:border-cyan transition-all duration-300 rounded-sm"
        >
          Contact
        </a>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-cyan p-2 -mr-2"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle Menu"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      <div
        className={`md:hidden transition-all duration-500 ease-in-out overflow-hidden border-t border-white/5 bg-bg/95 ${
          isOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="flex flex-col gap-4 p-6">
          <ul className="flex flex-col gap-4">
            {links.map((l) => (
              <li key={l.href}>
                <a
                  href={l.href}
                  onClick={() => setIsOpen(false)}
                  className="block font-syne text-[12px] text-text-dim hover:text-cyan tracking-[0.15em] uppercase transition-all duration-200"
                >
                  {l.label}
                </a>
              </li>
            ))}
          </ul>
          <a
            href="mailto:sumitmahato0913@gmail.com"
            onClick={() => setIsOpen(false)}
            className="w-full text-center font-syne text-[11px] font-bold tracking-[0.2em] uppercase px-6 py-3 border border-cyan/20 text-cyan hover:bg-cyan hover:text-bg hover:border-cyan transition-all duration-300 rounded-sm"
          >
            Contact
          </a>
        </div>
      </div>
    </nav>
  )
}
