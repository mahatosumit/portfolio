import { motion } from 'motion/react';
import { Card } from './ui/card';
import { 
  Brain, 
  Bot, 
  Code, 
  Database, 
  Settings,
  Cpu,
  Eye,
  Zap
} from 'lucide-react';

export function SkillsSection() {
  const skillCategories = [
    {
      title: 'AI/ML & Deep Learning',
      icon: Brain,
      skills: ['Computer Vision', 'TensorFlow', 'PyTorch', 'YOLOv8', 'CRNN'],
      color: 'from-purple-500 to-pink-500'
    },
    {
      title: 'Robotics & Embedded',
      icon: Bot,
      skills: ['ROS2', 'Arduino', 'STM32', 'Raspberry Pi', 'Pixhawk', 'IoT'],
      color: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Web Development',
      icon: Code,
      skills: ['React.js', 'Next.js', 'JavaScript', 'Tailwind', 'Bootstrap'],
      color: 'from-green-500 to-emerald-500'
    },
    {
      title: 'Data & Tools',
      icon: Database,
      skills: ['NumPy', 'Pandas', 'MATLAB', 'OpenCV', 'Grafana'],
      color: 'from-orange-500 to-red-500'
    },
    {
      title: 'System & Platforms',
      icon: Settings,
      skills: ['Git/GitHub', 'Linux', 'Windows', 'Docker', 'Cloud'],
      color: 'from-indigo-500 to-purple-500'
    },
    {
      title: 'Hardware Integration',
      icon: Cpu,
      skills: ['Microcontrollers', 'Sensors', 'Actuators', 'PCB Design', 'Protocols'],
      color: 'from-teal-500 to-blue-500'
    }
  ];

  return (
    <section id="skills" className="py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Technical <span className="text-primary">Skills</span>
          </h2>
          <div className="w-24 h-1 bg-primary mx-auto mb-8"></div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            A comprehensive toolkit spanning AI, robotics, and full-stack development
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {skillCategories.map((category, index) => (
            <motion.div
              key={category.title}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <Card className="p-6 h-full bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300 group hover:glow-effect">
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-r ${category.color} mr-4`}>
                    <category.icon size={24} className="text-white" />
                  </div>
                  <h3 className="text-xl font-semibold group-hover:text-primary transition-colors">
                    {category.title}
                  </h3>
                </div>
                
                <div className="space-y-3">
                  {category.skills.map((skill, skillIndex) => (
                    <motion.div
                      key={skill}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: (index * 0.1) + (skillIndex * 0.05) }}
                      className="flex items-center text-muted-foreground group-hover:text-foreground transition-colors"
                    >
                      <div className="w-2 h-2 bg-primary rounded-full mr-3 opacity-60"></div>
                      <span>{skill}</span>
                    </motion.div>
                  ))}
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Additional Skills Showcase */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-16 grid md:grid-cols-3 gap-8"
        >
          <Card className="p-6 text-center bg-card/30 backdrop-blur-sm border-border">
            <Eye size={40} className="mx-auto mb-4 text-primary" />
            <h4 className="text-lg font-semibold mb-2">Computer Vision</h4>
            <p className="text-muted-foreground text-sm">
              Object detection, image classification, and real-time processing
            </p>
          </Card>
          
          <Card className="p-6 text-center bg-card/30 backdrop-blur-sm border-border">
            <Zap size={40} className="mx-auto mb-4 text-primary" />
            <h4 className="text-lg font-semibold mb-2">Automation</h4>
            <p className="text-muted-foreground text-sm">
              Industrial automation and intelligent control systems
            </p>
          </Card>
          
          <Card className="p-6 text-center bg-card/30 backdrop-blur-sm border-border">
            <Settings size={40} className="mx-auto mb-4 text-primary" />
            <h4 className="text-lg font-semibold mb-2">System Integration</h4>
            <p className="text-muted-foreground text-sm">
              Hardware-software integration and IoT solutions
            </p>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}