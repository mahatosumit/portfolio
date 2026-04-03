import { motion } from "motion/react";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";

export function AboutSection() {
  const highlights = [
    "KrishiBot",
    "PlantFix",
    "Zunobot",
    "Chakravyuha",
  ];

  return (
    <section id="about" className="py-20 bg-muted/20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            About <span className="text-primary">Me</span>
          </h2>
          <div className="w-24 h-1 bg-primary mx-auto mb-8"></div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <Card className="p-8 bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300">
              <p className="text-lg leading-relaxed mb-6">
                I'm pursuing{" "}
                <span className="text-primary font-semibold">
                  B.E. Mechatronics Engineering
                </span>{" "}
                at KPRIET, Coimbatore. My journey started with
                UI/UX and web development, but I've since
                expanded into the fascinating worlds of AI/ML,
                Deep Learning, Robotics, and Embedded Systems.
              </p>

              <p className="text-lg leading-relaxed mb-6">
                I've worked on diverse projects spanning
                precision agriculture, intelligent mobility, and
                department-scale platforms. Each project has
                taught me something new about the intersection
                of hardware and software.
              </p>

              <div className="mb-6">
                <h4 className="text-xl font-semibold mb-4 text-primary">
                  Featured Projects:
                </h4>
                <div className="flex flex-wrap gap-2">
                  {highlights.map((project, index) => (
                    <motion.div
                      key={project}
                      initial={{ opacity: 0, scale: 0 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      viewport={{ once: true }}
                      transition={{
                        delay: index * 0.1,
                        duration: 0.5,
                      }}
                    >
                      <Badge
                        variant="secondary"
                        className="bg-primary/20 text-primary border-primary/30"
                      >
                        {project}
                      </Badge>
                    </motion.div>
                  ))}
                </div>
              </div>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="space-y-8"
          >
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300">
              <h4 className="text-xl font-semibold mb-4 text-primary">
                My Vision
              </h4>
              <p className="text-muted-foreground leading-relaxed">
                To bridge AI, robotics, and automation for
                scalable solutions in industry, agriculture, and
                smart mobility. I believe technology should
                solve real-world problems and make life better
                for everyone.
              </p>
            </Card>

            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border hover:border-primary transition-all duration-300">
              <h4 className="text-xl font-semibold mb-4 text-primary">
                Current Focus
              </h4>
              <ul className="space-y-2 text-muted-foreground">
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-primary rounded-full mr-3"></div>
                  Advanced Computer Vision Applications
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-primary rounded-full mr-3"></div>
                  Autonomous Robotics Systems
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-primary rounded-full mr-3"></div>
                  IoT & Embedded Systems Integration
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-primary rounded-full mr-3"></div>
                  Full-Stack Development
                </li>
              </ul>
            </Card>
          </motion.div>
        </div>
      </div>
    </section>
  );
}