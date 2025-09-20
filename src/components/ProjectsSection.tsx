import { motion } from 'motion/react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { ExternalLink, Github, ArrowRight } from 'lucide-react';
import zunobotImage from 'figma:asset/070d0f6597d2ce0f5396aa26cf6a9f3e0ce4b67c.png';

export function ProjectsSection() {
  const projects = [
    {
      title: 'Zunobot',
      description: 'STM32-based autonomous robotics project with advanced navigation and sensor integration capabilities.',
      image: zunobotImage,
      tags: ['STM32', 'Robotics', 'Autonomous', 'C++'],
      category: 'Robotics',
      featured: true
    },
    
    {
      title: 'KrishiBot',
      description: 'Smart crop recommendation system using machine learning to optimize agricultural yield and sustainability.',
      image: 'https://images.unsplash.com/photo-1722119272044-fc49006131e0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzbWFydCUyMGFncmljdWx0dXJlJTIwdGVjaG5vbG9neXxlbnwxfHx8fDE3NTgyOTM0NTN8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['Agriculture', 'ML', 'IoT', 'Sustainability'],
      category: 'Agriculture',
      featured: true
    },
    {
      title: 'PlantFix',
      description: 'Plant species & health detection system using YOLOv8 for real-time disease identification and treatment recommendations.',
      image: 'https://images.unsplash.com/photo-1716725330092-be290229e5f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwbGFudCUyMGRpc2Vhc2UlMjBkZXRlY3Rpb258ZW58MXx8fHwxNzU4MjkzNDU4fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['YOLOv8', 'Computer Vision', 'Healthcare', 'Agriculture'],
      category: 'AI/ML',
      featured: false
    },
    {
      title: 'Chakravyuha',
      description: 'Official hackathon website of KPRIET Mechatronics Department with registration and event management system.',
      image: 'https://images.unsplash.com/photo-1603985585179-3d71c35a537c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3ZWIlMjBkZXZlbG9wbWVudCUyMHdvcmtzcGFjZXxlbnwxfHx8fDE3NTgyNjkxMzR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['React', 'Next.js', 'Web Dev', 'Event Management'],
      category: 'Web Development',
      featured: false
    },
    {
      title: 'Music Auto-Tagging CRNN',
      description: 'Convolutional Recurrent Neural Network for automatic music genre and mood recognition with high accuracy.',
      image: 'https://images.unsplash.com/photo-1603985585179-3d71c35a537c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3ZWIlMjBkZXZlbG9wbWVudCUyMHdvcmtzcGFjZXxlbnwxfHx8fDE3NTgyNjkxMzR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['CRNN', 'Deep Learning', 'Audio Processing', 'TensorFlow'],
      category: 'AI/ML',
      featured: false
    }
  ];

  const categories = ['All', 'AI/ML', 'Robotics', 'Web Development', 'Agriculture'];

  return (
    <section id="projects" className="py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Latest <span className="text-primary">Projects</span>
          </h2>
          <div className="w-24 h-1 bg-primary mx-auto mb-8"></div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Innovative solutions spanning AI, robotics, and web development
          </p>
        </motion.div>

        {/* Category Filter */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="flex flex-wrap justify-center gap-4 mb-12"
        >
          {categories.map((category) => (
            <Button 
              key={category}
              variant="outline"
              className="hover:bg-primary hover:text-primary-foreground transition-all duration-300"
            >
              {category}
            </Button>
          ))}
        </motion.div>

        {/* Featured Projects */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold mb-8 text-center">Featured Projects</h3>
          <div className="grid lg:grid-cols-3 gap-8">
            {projects.filter(p => p.featured).map((project, index) => (
              <motion.div
                key={project.title}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
              >
                <Card className="overflow-hidden bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300 group hover:glow-effect">
                  <div className="relative overflow-hidden">
                    {typeof project.image === 'string' ? (
                      <ImageWithFallback
                        src={project.image}
                        alt={project.title}
                        className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    ) : (
                      <img
                        src={project.image}
                        alt={project.title}
                        className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex gap-2">
                      <Button size="icon" variant="secondary" className="w-8 h-8">
                        <Github size={16} />
                      </Button>
                      <Button size="icon" variant="secondary" className="w-8 h-8">
                        <ExternalLink size={16} />
                      </Button>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-xl font-semibold group-hover:text-primary transition-colors">
                        {project.title}
                      </h3>
                      <Badge variant="secondary" className="text-xs">
                        {project.category}
                      </Badge>
                    </div>
                    
                    <p className="text-muted-foreground mb-4 text-sm leading-relaxed">
                      {project.description}
                    </p>
                    
                    <div className="flex flex-wrap gap-2 mb-4">
                      {project.tags.map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs bg-primary/10 border-primary/30">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300"
                    >
                      View Details
                      <ArrowRight size={14} className="ml-2" />
                    </Button>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Other Projects */}
        <div>
          <h3 className="text-2xl font-bold mb-8 text-center">More Projects</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.filter(p => !p.featured).map((project, index) => (
              <motion.div
                key={project.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className="p-6 bg-card/30 backdrop-blur-sm border-border hover:border-primary transition-all duration-300 group hover:glow-effect">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold group-hover:text-primary transition-colors">
                      {project.title}
                    </h4>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button size="icon" variant="ghost" className="w-6 h-6">
                        <Github size={12} />
                      </Button>
                      <Button size="icon" variant="ghost" className="w-6 h-6">
                        <ExternalLink size={12} />
                      </Button>
                    </div>
                  </div>
                  
                  <p className="text-muted-foreground text-sm mb-4 leading-relaxed">
                    {project.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-1">
                    {project.tags.slice(0, 3).map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs bg-primary/10">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mt-16"
        >
          <a 
  href="https://github.com/mahatosumit" 
  target="_blank" 
  rel="noopener noreferrer"
>
  <Button size="lg" className="glow-effect">
    View All Projects on GitHub
    <Github size={20} className="ml-2" />
  </Button>
</a>
        </motion.div>
      </div>
    </section>
  );
}