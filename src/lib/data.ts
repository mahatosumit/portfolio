export const PROFILE = {
  name: 'Sumit Mahato',
  role: 'Autonomous Systems Engineer',
  tagline: 'Robotics · ADAS · AI',
  headline: 'I Build Systems That See, Think, and Drive Themselves',
  subtext:
    'I design and engineer autonomous systems across robotics, ADAS, and AI — built for real-world deployment, not simulations.',
  email: 'sumitmahato0913@gmail.com',
  phone: '+919363962670',
  website: 'https://sumitmahato.com.np',
  github: 'https://github.com/mahatosumit',
  linkedin: 'https://linkedin.com/in/mahatosumit',
  kaggle: 'https://kaggle.com/mahatosumit',
  optinx: 'https://optinx.space/',
  location: 'Arasur, Coimbatore',
}

export const PROOF_STRIP = [
  { label: 'Bosch Future Mobility Challenge Finalist', detail: 'Top 22 Global' },
  { label: 'ADAS Systems', detail: 'Lane Detection · Drowsiness Detection · Navigation' },
  { label: 'Robotics + Embedded', detail: 'STM32, Raspberry Pi, ROS2' },
  { label: 'AI Systems', detail: 'YOLO, CRNN, TensorFlow, XGBoost' },
]

export const METRICS = [
  { value: '6+', label: 'Real Systems\nEngineered' },
  { value: '3+', label: 'AI Production-Level\nProjects' },
  { value: 'ADAS\n+ROS', label: 'Autonomous\nStacks Built' },
  { value: 'Bosch\nBFMC', label: 'International\nFinalist' },
]

export const CAPABILITIES = [
  {
    num: '01',
    title: 'Autonomous Systems',
    arrow: 'Robots with navigation, control, and decision-making',
    desc: 'Full-stack autonomy: perception → planning → execution. Hardware-grounded.',
  },
  {
    num: '02',
    title: 'Computer Vision Systems',
    arrow: 'Real-time perception using YOLO, CRNN',
    desc: 'Object detection, classification, and tracking pipelines deployed at the edge.',
  },
  {
    num: '03',
    title: 'Embedded Intelligence',
    arrow: 'STM32, Raspberry Pi, sensor integration',
    desc: 'AI inference on constrained hardware. Sensor fusion, PWM, motor control.',
  },
  {
    num: '04',
    title: 'AI Systems',
    arrow: 'Deep learning pipelines, classification, detection',
    desc: 'From dataset to deployment — TensorFlow, YOLO, RAG, XGBoost.',
  },
]

export const EXPERIENCE = [
  {
    org: 'Bosch',
    role: 'RAG Intern',
    period: 'Internship',
    problem: 'Unstructured data limiting AI usability',
    system: 'Retrieval-Augmented Generation pipeline for structured knowledge access from enterprise data.',
    impact: 'Efficient querying + improved AI response relevance across internal knowledge bases.',
  },
  {
    org: 'Bosch BFMC',
    role: 'Global Finalist',
    period: 'Top 22 Worldwide',
    problem: 'Autonomous driving in constrained environments',
    system: 'Full ADAS stack: lane detection, parking assistance, overtaking logic — on a miniature autonomous vehicle.',
    impact: 'Selected among top 22 global teams in Bosch\'s international autonomous driving challenge.',
  },
  {
    org: 'KKR Robotics',
    role: 'ROS Developer Intern',
    period: 'Internship',
    problem: 'Robot control and simulation integration',
    system: 'ROS2 communication system with differential drive navigation and Gazebo simulation using URDF.',
    impact: 'Real-time robotic control and simulation-to-hardware pipeline enabled.',
  },
  {
    org: 'Mayagreens',
    role: 'AI Intern',
    period: 'Agriculture Tech',
    problem: 'Plant identification and monitoring at scale',
    system: 'Computer vision classification model + Grafana sensor dashboard + Vue3 push notification system.',
    impact: 'Automated plant monitoring with live data visualization.',
  },
]

export const STACK = [
  {
    layer: 'AI Layer',
    items: ['YOLOv8 / v11', 'TensorFlow', 'CRNN', 'Scikit-learn', 'XGBoost', 'RAG Pipelines'],
  },
  {
    layer: 'System Layer',
    items: ['ROS2', 'Gazebo', 'URDF', 'OpenCV', 'Grafana', 'Vue3.js'],
  },
  {
    layer: 'Hardware Layer',
    items: ['STM32', 'Raspberry Pi 5', 'Pixhawk', 'Ultrasonic Sensors', 'L298N Motor Driver'],
  },
  {
    layer: 'Programming',
    items: ['Python', 'C', 'JavaScript', 'TypeScript', 'URDF / XML'],
  },
]

export const PROJECTS = [
  {
    num: '01',
    name: 'ZUNO',
    role: 'Autonomous Assistive Robot',
    pipeline: ['Camera', 'Sensor Input', 'STM32 Control', 'Motion Execution'],
    tech: ['Python', 'OpenCV', 'Raspberry Pi 5', 'STM32', 'Ultrasonic', 'L298N'],
    impact: 'Real-time navigation + obstacle avoidance',
    github: '',
  },
  {
    num: '02',
    name: 'DrowseGuard',
    role: 'Drowsiness Detection — ADAS',
    pipeline: ['Camera', 'YOLOv8 Model', 'Eye Detection', 'Alert System'],
    tech: ['Python', 'OpenCV', 'YOLOv8'],
    impact: 'Driver fatigue detection → safety alert pipeline',
    github: 'https://github.com/mahatosumit',
  },
  {
    num: '03',
    name: 'KrishiBot',
    role: 'Smart Crop Recommendation Engine',
    pipeline: ['Sensor Data', 'XGBoost Model', 'Crop Recommendation'],
    tech: ['Python', 'XGBoost', 'Scikit-learn', 'Weather API', 'Google Translate'],
    impact: 'Data-driven agriculture with multilingual support',
    github: 'https://krishibot.netlify.app/',
  },
  {
    num: '04',
    name: 'PlantFix',
    role: 'Plant Classification System',
    pipeline: ['Image Input', 'YOLO Model', 'Classification Output'],
    tech: ['YOLOv8', 'TensorFlow', 'OpenCV', 'Keras'],
    impact: '300K+ images — 1,000 species, scalable plant monitoring',
    github: 'https://github.com/mahatosumit',
  },
  {
    num: '05',
    name: 'Music Auto-Tagger',
    role: 'CRNN Audio Classification',
    pipeline: ['Audio Input', 'Mel Spectrogram', 'CRNN Model', 'Multi-label Output'],
    tech: ['Python', 'TensorFlow', 'Keras', 'CRNN'],
    impact: '25K+ samples, 50 tags — genre and mood detection',
    github: 'https://github.com/mahatosumit',
  },
  {
    num: '06',
    name: 'Chakravyuha',
    role: 'National Fest Platform',
    pipeline: ['Event Data', 'Registration System', 'Real-time Dashboard'],
    tech: ['HTML', 'Tailwind CSS', 'JavaScript', 'Bootstrap'],
    impact: 'IEEE RAS + VTS national-level fest, students nationwide',
    github: 'https://chakravyuha.kpriet.ac.in/',
  },
]

export const NEXT_BUILDS = [
  { name: 'TravaX', desc: 'Campus-scale ADAS system', status: 'Active' },
  { name: 'Autonomy Platform', desc: 'Modular robotics + autonomy framework', status: 'Building' },
  { name: 'AI + RAG', desc: 'Production-grade retrieval systems', status: 'Research' },
  { name: 'OPTINX Ecosystem', desc: 'AI + automation across mobility and agriculture', status: 'Expanding' },
]

export const OPTINX_PILLARS = [
  'Autonomous Mobility Systems',
  'Agricultural Intelligence',
  'Robotics & Embedded AI',
  'RAG & Knowledge Systems',
  'Edge AI Deployment',
]

export const MINDSET = [
  'I build systems, not demos.',
  'Real-world constraints drive design.',
  'Scalability over shortcuts.',
  'Execution over ideas.',
]

export const CERTIFICATIONS = [
  'Introduction to Self-Driving Car (Oct 2025)',
  'State Estimation & Localization for Self-Driving Car',
  'Advanced Driver Assistance Systems (ADAS)',
  'Fundamentals of Accelerated Computing — Python',
  'Fundamentals of Accelerated Computing — CUDA C/C++',
  'Deep Learning with PyTorch',
  'Robo-AI: Industrial Training on Robotics & AI',
]

export const AWARDS = [
  { award: '2nd Runner-Up', event: 'Prompt-It Right', year: 'Sep 2025' },
  { award: 'Runner-Up', event: 'Pitch Up Competition', year: 'Sep 2024' },
  { award: 'Best Project Award', event: 'College Science Day', year: 'Feb 2024' },
  { award: '1st Rank', event: 'Hetauda Sub-metropolitan Science Exhibition', year: 'Feb 2019' },
]
