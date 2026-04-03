import { PROFILE } from '@/lib/data'
import { Github, Linkedin, Globe, Mail } from 'lucide-react'

const socials = [
  { href: PROFILE.github, icon: Github, label: 'GitHub' },
  { href: PROFILE.linkedin, icon: Linkedin, label: 'LinkedIn' },
  { href: PROFILE.optinx, icon: Globe, label: 'OPTINX' },
  { href: `mailto:${PROFILE.email}`, icon: Mail, label: 'Email' },
]

const navLinks = [
  { href: '#build', label: 'Build' },
  { href: '#delivered', label: 'Delivered' },
  { href: '#stack', label: 'Stack' },
  { href: '#projects', label: 'Projects' },
  { href: '#optinx', label: 'OPTINX' },
]

export default function Footer() {
  return (
    <footer className="border-t border-white/5 px-6 md:px-12 py-16 max-w-7xl mx-auto">
      <div className="grid md:grid-cols-3 gap-12 mb-12">
        {/* Brand */}
        <div>
          <div className="font-syne text-2xl font-extrabold tracking-tight mb-2">
            Sumit <span className="text-cyan">Mahato</span>
          </div>
          <div className="font-mono text-[11px] text-text-dim mb-6 tracking-wider">
            Autonomous Systems · ADAS · Robotics · AI
          </div>
          <a
            href={PROFILE.optinx}
            target="_blank"
            rel="noopener noreferrer"
            className="font-mono text-[11px] text-cyan/60 hover:text-cyan transition-colors duration-200"
          >
            Founder @ OPTINX →
          </a>
        </div>

        {/* Nav */}
        <div>
          <div className="font-mono text-[10px] text-text-dim uppercase tracking-[0.2em] mb-5">Navigation</div>
          <ul className="flex flex-col gap-3">
            {navLinks.map(l => (
              <li key={l.href}>
                <a
                  href={l.href}
                  className="font-mono text-[12px] text-text-dim hover:text-cyan transition-colors duration-200 tracking-wide"
                >
                  {l.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        {/* Contact */}
        <div>
          <div className="font-mono text-[10px] text-text-dim uppercase tracking-[0.2em] mb-5">Connect</div>
          <div className="flex flex-col gap-3">
            {socials.map(s => (
              <a
                key={s.label}
                href={s.href}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 font-mono text-[12px] text-text-dim hover:text-cyan transition-colors duration-200 group"
              >
                <s.icon size={13} className="group-hover:text-cyan transition-colors" />
                {s.label}
              </a>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom */}
      <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="font-mono text-[10px] text-text-dim tracking-wider">
          © {new Date().getFullYear()} Sumit Kumar Mahato. Built with Next.js 14.
        </div>
        <div className="font-mono text-[10px] text-text-dim tracking-wider">
          {PROFILE.location}
        </div>
      </div>
    </footer>
  )
}
