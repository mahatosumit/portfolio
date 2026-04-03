import Nav from '@/components/Nav'
import Hero from '@/components/Hero'
import Metrics from '@/components/Metrics'
import Capabilities from '@/components/Capabilities'
import Experience from '@/components/Experience'
import StackSection from '@/components/StackSection'
import Projects from '@/components/Projects'
import NextBuilds from '@/components/NextBuilds'
import Optinx from '@/components/Optinx'
import AwardsCerts from '@/components/AwardsCerts'
import MindsetSection from '@/components/MindsetSection'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="grid-bg min-h-screen">
      <Nav />

      {/* Ambient radial glow top */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-cyan/[0.03] blur-[100px] pointer-events-none z-0" />

      <div className="relative z-10">
        <Hero />
        <Metrics />
        <Capabilities />
        <Experience />
        <StackSection />
        <Projects />
        <NextBuilds />
        <Optinx />
        <AwardsCerts />
        <MindsetSection />
        <Footer />
      </div>
    </main>
  )
}
