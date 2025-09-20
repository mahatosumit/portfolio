import { motion } from 'motion/react';
import { Github, Linkedin, Globe, ChevronDown } from 'lucide-react';
import { Button } from './ui/button';
import heroImage from 'figma:asset/0880421087ec693b7c4eb12ae59cd905e6a0bd5d.png';

export function HeroSection() {
  const socialLinks = [
    { icon: Github, href: 'https://github.com/mahatosumit', label: 'GitHub' },
    { icon: Linkedin, href: 'https://www.linkedin.com/in/mahatosumit/', label: 'LinkedIn' },
  ];

  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background Grid Pattern */}
      <div className="absolute inset-0 grid-pattern opacity-30"></div>

      <div className="container mx-auto px-4 py-20 grid lg:grid-cols-2 gap-12 items-center relative z-10">
        {/* Left Content */}
        <div className="space-y-6">
          <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
            Hi, I'm{' '}
            <span className="text-primary">Sumit Mahato</span>
          </h1>
          
          <h2 className="text-xl lg:text-2xl text-muted-foreground">
            🚀 Mechatronics Engineer | AI & Robotics Researcher | Developer | Innovator
          </h2>

          <p className="text-lg text-muted-foreground max-w-lg">
            Turning AI & Robotics into Real-World Automation.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button size="lg" className="glow-effect">
              View My Work
            </Button>
            <Button variant="outline" size="lg">
              Download CV
            </Button>
          </div>

          {/* Social Links */}
          <div className="flex space-x-6">
            {socialLinks.map((social) => (
              <a
                key={social.label}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 bg-card border border-border rounded-lg hover:border-primary transition-all duration-300 hover:glow-effect hover:scale-110"
              >
                <social.icon size={20} />
              </a>
            ))}
          </div>
        </div>

        {/* Right Content - Profile Image */}
        <div className="flex justify-center lg:justify-end">
          <div className="hexagon glow-effect hover:scale-105 transition-transform duration-300">
            <div className="hexagon-inner">
              <img
                src={heroImage}
                alt="Sumit Kumar Mahato"
                className="hexagon-img"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
        <div className="flex flex-col items-center text-muted-foreground animate-bounce">
          <span className="text-sm mb-2">Scroll Down</span>
          <ChevronDown size={20} />
        </div>
      </div>
    </section>
  );
}