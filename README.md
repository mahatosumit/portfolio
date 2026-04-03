# Sumit Mahato — Engineering Identity Platform

Built with **Next.js 14**, **TypeScript**, **Tailwind CSS**, **Framer Motion**, and **Lucide React**.

## Tech Stack

| Layer | Tech |
|---|---|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS v3 |
| Animation | Framer Motion + CSS animations |
| Icons | Lucide React |
| Fonts | Syne (display) · JetBrains Mono · DM Sans |
| Canvas | Vanilla Canvas API (system UI animation) |
| Export | Static export (`output: 'export'`) |

## Getting Started

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview static export
npx serve out
```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx        # Root layout + fonts + metadata
│   ├── page.tsx          # Page assembly
│   └── globals.css       # Global styles + Tailwind
├── components/
│   ├── Nav.tsx           # Sticky nav with scroll detection
│   ├── Hero.tsx          # Hero + CTAs
│   ├── SystemCanvas.tsx  # Animated canvas system UI
│   ├── Metrics.tsx       # Animated proof metrics
│   ├── Capabilities.tsx  # What I Build (4 cards)
│   ├── Experience.tsx    # Systems Delivered (4 rows)
│   ├── StackSection.tsx  # Engineering stack layers
│   ├── Projects.tsx      # 6 project cards with pipeline
│   ├── NextBuilds.tsx    # Roadmap with status indicators
│   ├── Optinx.tsx        # OPTINX venture section
│   ├── AwardsCerts.tsx   # Awards + Certifications
│   ├── MindsetSection.tsx# Engineering mindset
│   ├── Footer.tsx        # Footer with links
│   └── SectionTag.tsx    # Reusable section tag
└── lib/
    ├── data.ts           # All content data (single source of truth)
    └── useInView.ts      # Scroll intersection hook
```

## Customization

All content lives in `src/lib/data.ts`. Edit that file to update:
- Profile info (email, links, location)
- Proof strip items
- Experience entries
- Projects
- Stack items
- Certifications and awards

## Deployment

This project uses `output: 'export'` in `next.config.js`, generating a static site in `/out`.

Deploy to:
- **Vercel** — `vercel deploy` (recommended, just connect the repo)
- **Netlify** — drag and drop the `/out` folder
- **GitHub Pages** — push `/out` to `gh-pages` branch
- **Custom server** — serve the `/out` folder with nginx/caddy

## Design System

- **Colors**: `#030508` (bg), `#00ffb4` (cyan accent), `#00ff88` (green)
- **Fonts**: Syne 800 (headlines), JetBrains Mono (labels/code), DM Sans (body)
- **Theme**: Deep dark, minimal cards, asymmetric layouts, subtle cyan glow
- **Motion**: Scroll-triggered fade-ups, canvas animation, hover micro-interactions
