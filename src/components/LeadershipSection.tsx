import { motion } from 'motion/react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Users, 
  Trophy, 
  Target, 
  Heart,
  Code,
  Award
} from 'lucide-react';

export function LeadershipSection() {
  const positions = [
    {
      title: 'Executive Member & Technical Lead',
      organization: 'IEEE VTS, KPRIET',
      period: '2023 - 2024',
      description: 'Leading technical initiatives and organizing workshops on emerging technologies in vehicular technology.',
      icon: Users,
      achievements: [
        'Organized 5+ technical workshops',
        'Led team of 15+ members',
        'Increased membership by 40%'
      ]
    },
    {
      title: 'Website Developer',
      organization: 'Chakravyuha Hackathon',
      period: '2025',
      description: 'Developed the official website and registration system for the college\'s flagship hackathon event.',
      icon: Code,
      achievements: [
        '500+ registrations processed',
        'Real-time leaderboard system',
        'Responsive design implementation'
      ]
    },
    {
      title: 'Open Source Contributor',
      organization: 'GitHub, Medium, Kaggle',
      period: '2022 - Present',
      description: 'Active contributor to open-source projects and knowledge sharing through technical articles.',
      icon: Heart,
      achievements: [
        '20+ GitHub repositories',
        '15+ technical articles',
        '1000+ profile views'
      ]
    }
  ];

  const achievements = [
    {
      title: 'Runner-Up',
      event: 'Prompt-it Right 2025',
      description: 'Prompted to get the actual output',
      icon: Trophy,
      color: 'from-yellow-500 to-orange-500'
    },{
      title: 'Runner-Up',
      event: 'Pitch Up Competition 2024',
      description: 'Presented innovative solution for smart learning kit for children',
      icon: Trophy,
      color: 'from-yellow-500 to-orange-500'
    },
    {
      title: 'Best Project',
      event: 'College Science Day 2024',
      description: 'Recognized for outstanding project in mechatronics engineering',
      icon: Award,
      color: 'from-blue-500 to-purple-500'
    },
    {
      title: '1st Rank',
      event: 'Hetauda Science Exhibition 2019',
      description: 'Won first place in sub-metropolitan science exhibition',
      icon: Target,
      color: 'from-green-500 to-emerald-500'
    }
  ];

  const certifications = [
    'ADAS & Autonomous Driving',
    'Advanced Robotics Systems',
    'Robo AI : Industrial Training Program on Robotics and AI',
    'Deep Learning Specialization',
    'MATLAB Programming',
    'CUDA Programming',
    'ROS2 Development'
  ];

  return (
    <section id="leadership" className="py-20 bg-muted/20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Leadership & <span className="text-primary">Community</span>
          </h2>
          <div className="w-24 h-1 bg-primary mx-auto mb-8"></div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Building communities, leading initiatives, and sharing knowledge
          </p>
        </motion.div>

        {/* Leadership Positions */}
        <div className="mb-20">
          <h3 className="text-2xl font-bold mb-8 text-center">Leadership Positions</h3>
          <div className="grid lg:grid-cols-3 gap-8">
            {positions.map((position, index) => (
              <motion.div
                key={position.title}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
              >
                <Card className="p-6 h-full bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300 group hover:glow-effect">
                  <div className="flex items-center mb-4">
                    <div className="p-3 bg-primary/20 rounded-lg mr-4">
                      <position.icon size={24} className="text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold group-hover:text-primary transition-colors">
                        {position.title}
                      </h4>
                      <p className="text-sm text-muted-foreground">{position.organization}</p>
                    </div>
                  </div>
                  
                  <Badge variant="outline" className="mb-4 bg-primary/10 border-primary/30">
                    {position.period}
                  </Badge>
                  
                  <p className="text-muted-foreground mb-4 leading-relaxed">
                    {position.description}
                  </p>
                  
                  <div className="space-y-2">
                    <h5 className="font-semibold text-sm">Key Achievements:</h5>
                    {position.achievements.map((achievement, idx) => (
                      <motion.div
                        key={achievement}
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: (index * 0.2) + (idx * 0.1) }}
                        className="flex items-center text-sm text-muted-foreground"
                      >
                        <div className="w-1.5 h-1.5 bg-primary rounded-full mr-3"></div>
                        <span>{achievement}</span>
                      </motion.div>
                    ))}
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Achievements */}
        <div className="mb-20">
          <h3 className="text-2xl font-bold mb-8 text-center">Achievements & Recognition</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {achievements.map((achievement, index) => (
              <motion.div
                key={achievement.title}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
              >
                <Card className="p-6 text-center bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300 hover:glow-effect">
                  <div className={`w-16 h-16 bg-gradient-to-r ${achievement.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
                    <achievement.icon size={32} className="text-white" />
                  </div>
                  
                  <h4 className="text-xl font-semibold mb-2">{achievement.title}</h4>
                  <p className="text-primary font-medium mb-3">{achievement.event}</p>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {achievement.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Certifications */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h3 className="text-2xl font-bold mb-8 text-center">Certifications & Training</h3>
          <Card className="p-8 bg-card/30 backdrop-blur-sm border-border">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {certifications.map((cert, index) => (
                <motion.div
                  key={cert}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center p-3 bg-primary/10 rounded-lg border border-primary/20 hover:border-primary/40 transition-colors"
                >
                  <div className="w-2 h-2 bg-primary rounded-full mr-3"></div>
                  <span className="text-sm font-medium">{cert}</span>
                </motion.div>
              ))}
            </div>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}