import { motion } from 'motion/react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { 
  Brain, 
  Bot, 
  Code, 
  Palette, 
  Calendar,
  ArrowRight
} from 'lucide-react';

export function ServicesSection() {
  const services = [
    {
      title: 'AI & Computer Vision Solutions',
      description: 'Custom AI models for object detection, image classification, and real-time video analysis using state-of-the-art deep learning frameworks.',
      icon: Brain,
      features: ['YOLOv8 Implementation', 'Custom CNN Models', 'Real-time Processing', 'Edge Deployment'],
      color: 'from-purple-500 to-pink-500'
    },
    {
      title: 'Robotics & Embedded Systems',
      description: 'End-to-end robotics solutions from concept to deployment, including autonomous navigation, sensor integration, and control systems.',
      icon: Bot,
      features: ['ROS2 Development', 'Autonomous Navigation', 'Sensor Fusion', 'Hardware Integration'],
      color: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Web Development',
      description: 'Modern web applications with responsive design, seamless user experience, and scalable backend architecture.',
      icon: Code,
      features: ['React/Next.js', 'API Development', 'Database Design', 'Cloud Deployment'],
      color: 'from-green-500 to-emerald-500'
    },
    {
      title: 'UI/UX Design',
      description: 'User-centered design solutions that combine aesthetics with functionality to create engaging digital experiences.',
      icon: Palette,
      features: ['Wireframing', 'Prototyping', 'User Research', 'Design Systems'],
      color: 'from-orange-500 to-red-500'
    },
    {
      title: 'Event Tech Solutions',
      description: 'Complete technical solutions for hackathons and events, including websites, registration systems, and live platforms.',
      icon: Calendar,
      features: ['Event Websites', 'Registration Systems', 'Live Dashboards', 'Tech Support'],
      color: 'from-indigo-500 to-purple-500'
    }
  ];

  return (
    <section id="services" className="py-20 bg-muted/20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            My <span className="text-primary">Services</span>
          </h2>
          <div className="w-24 h-1 bg-primary mx-auto mb-8"></div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Transforming ideas into intelligent solutions across multiple domains
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <Card className="p-6 h-full bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300 group hover:glow-effect hover:scale-105">
                {/* Service Icon */}
                <div className="flex items-center mb-6">
                  <div className={`p-4 rounded-xl bg-gradient-to-r ${service.color} mr-4`}>
                    <service.icon size={32} className="text-white" />
                  </div>
                  <h3 className="text-xl font-semibold group-hover:text-primary transition-colors">
                    {service.title}
                  </h3>
                </div>

                {/* Service Description */}
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  {service.description}
                </p>

                {/* Service Features */}
                <div className="space-y-3 mb-6">
                  {service.features.map((feature, featureIndex) => (
                    <motion.div
                      key={feature}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: (index * 0.1) + (featureIndex * 0.05) }}
                      className="flex items-center text-sm text-muted-foreground"
                    >
                      <div className="w-1.5 h-1.5 bg-primary rounded-full mr-3"></div>
                      <span>{feature}</span>
                    </motion.div>
                  ))}
                </div>

                {/* CTA Button */}
                <Button 
                  variant="outline" 
                  className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300"
                >
                  Learn More
                  <ArrowRight size={16} className="ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Service Process */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mt-20"
        >
          <h3 className="text-3xl font-bold text-center mb-12">
            My <span className="text-primary">Process</span>
          </h3>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { step: '01', title: 'Discovery', desc: 'Understanding your requirements and goals' },
              { step: '02', title: 'Design', desc: 'Creating the blueprint and architecture' },
              { step: '03', title: 'Development', desc: 'Building with cutting-edge technologies' },
              { step: '04', title: 'Delivery', desc: 'Testing, deployment, and ongoing support' }
            ].map((process, index) => (
              <motion.div
                key={process.step}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-primary/20 border-2 border-primary rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary font-bold text-lg">{process.step}</span>
                </div>
                <h4 className="text-lg font-semibold mb-2">{process.title}</h4>
                <p className="text-muted-foreground text-sm">{process.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
