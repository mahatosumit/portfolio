import { Github, Linkedin, Globe, Heart } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  const socialLinks = [
    {
      icon: Github,
      href: "https://github.com/mahatosumit/",
      label: "GitHub",
    },
    {
      icon: Linkedin,
      href: "https://www.linkedin.com/in/mahatosumit/",
      label: "LinkedIn",
    },
  ];

  const quickLinks = [
    { name: "About", href: "#about" },
    { name: "Skills", href: "#skills" },
    { name: "Projects", href: "#projects" },
    { name: "Contact", href: "#contact" },
  ];

  return (
    <footer className="bg-card/30 backdrop-blur-sm border-t border-border">
      <div className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Brand Section */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-primary">
              Sumit Mahato
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              Mechatronics Engineer passionate about AI,
              Robotics, and creating intelligent solutions for
              real-world problems.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 bg-muted rounded-lg hover:bg-primary/20 hover:text-primary transition-all duration-300 hover:scale-110"
                >
                  <social.icon size={18} />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">
              Quick Links
            </h4>
            <div className="space-y-2">
              {quickLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="block text-muted-foreground hover:text-primary transition-colors duration-300"
                >
                  {link.name}
                </a>
              ))}
            </div>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">
              Get In Touch
            </h4>
            <div className="space-y-2 text-muted-foreground">
              <p>Coimbatore, India</p>
              <p>www.mahatosumit.com.np</p>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-muted-foreground text-sm">
            © {currentYear} Sumit Mahato. All rights reserved.
          </p>
          <div className="flex items-center text-muted-foreground text-sm mt-4 md:mt-0">
            <span>Made with</span>
            <Heart size={16} className="mx-2 text-red-500" />
            <span>in Technology</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
