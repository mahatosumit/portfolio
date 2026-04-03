import type { Metadata } from 'next'
import { Syne, JetBrains_Mono, Inter } from 'next/font/google'
import './globals.css'

const syne = Syne({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-syne',
  display: 'swap',
})

const jetbrains = JetBrains_Mono({
  subsets: ['latin'],
  weight: ['300', '400', '500'],
  variable: '--font-jetbrains',
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Sumit Mahato — Autonomous Systems Engineer',
  description: 'I build systems that see, think, and drive themselves. Autonomous Systems Engineer specializing in Robotics, ADAS, and AI.',
  keywords: ['Autonomous Systems', 'Robotics', 'ADAS', 'Computer Vision', 'AI Engineer', 'Sumit Mahato'],
  openGraph: {
    title: 'Sumit Mahato — Autonomous Systems Engineer',
    description: 'Building intelligent systems across robotics, ADAS, and AI.',
    url: 'https://sumitmahato.com.np',
    siteName: 'Sumit Mahato',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${syne.variable} ${jetbrains.variable} ${inter.variable}`}>
      <body>
        <div className="noise-overlay" aria-hidden="true" />
        {children}
      </body>
    </html>
  )
}
