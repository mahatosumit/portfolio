'use client'
import { useEffect, useRef } from 'react'

const C = 'rgba(0,212,170,'
const G = 'rgba(34,211,238,'

interface Node {
  x: number; y: number; vx: number; vy: number
  size: number; pulse: number; pulseSpeed: number
  minX: number; maxX: number; minY: number; maxY: number
}

interface Packet {
  from: Node; to: Node; t: number; speed: number
}

export default function SystemCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    let frame = 0
    let raf: number
    let scanY = 0
    let scanDir = 1

    const makeNode = (x: number, y: number, range: number, speed: number): Node => ({
      x, y,
      vx: (Math.random() - 0.5) * speed,
      vy: (Math.random() - 0.5) * speed,
      size: 2 + Math.random() * 2.5,
      pulse: Math.random() * Math.PI * 2,
      pulseSpeed: 0.025 + Math.random() * 0.025,
      minX: x - range, maxX: x + range,
      minY: y - range, maxY: y + range,
    })

    function resize() {
      const W = canvas!.parentElement!.clientWidth
      const H = canvas!.parentElement!.clientHeight
      canvas!.width = W; canvas!.height = H
    }
    resize()
    const ro = new ResizeObserver(resize)
    ro.observe(canvas.parentElement!)

    // Build nodes along outer ring
    const outer: Node[] = Array.from({ length: 14 }, (_, i) => {
      const a = (i / 14) * Math.PI * 2
      const W = canvas.width, H = canvas.height
      const cx = W / 2, cy = H / 2
      const r = Math.min(W, H) * 0.36
      return makeNode(cx + Math.cos(a) * r, cy + Math.sin(a) * r, 18, 0.3)
    })

    const inner: Node[] = Array.from({ length: 6 }, (_, i) => {
      const a = (i / 6) * Math.PI * 2
      const W = canvas.width, H = canvas.height
      const cx = W / 2, cy = H / 2
      const r = Math.min(W, H) * 0.14
      return makeNode(cx + Math.cos(a) * r, cy + Math.sin(a) * r, 10, 0.25)
    })

    const packets: Packet[] = []
    const iv = setInterval(() => {
      if (packets.length < 8) {
        const from = outer[Math.floor(Math.random() * outer.length)]
        const to = outer[Math.floor(Math.random() * outer.length)]
        if (from !== to) packets.push({ from, to, t: 0, speed: 0.006 + Math.random() * 0.01 })
      }
    }, 350)

    let targetX = 0, targetY = 0, tdx = 0.4, tdy = 0.3

    function draw() {
      const W = canvas!.width, H = canvas!.height
      ctx.clearRect(0, 0, W, H)
      const cx = W / 2, cy = H / 2

      // Grid
      ctx.strokeStyle = C + '0.04)'
      ctx.lineWidth = 0.5
      const step = 48
      for (let x = 0; x < W; x += step) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke() }
      for (let y = 0; y < H; y += step) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke() }

      // Scan
      scanY += scanDir * 1.5
      if (scanY > H) scanDir = -1
      if (scanY < 0) scanDir = 1
      const sg = ctx.createLinearGradient(0, scanY - 40, 0, scanY + 40)
      sg.addColorStop(0, C + '0)')
      sg.addColorStop(0.5, C + '0.05)')
      sg.addColorStop(1, C + '0)')
      ctx.fillStyle = sg
      ctx.fillRect(0, scanY - 40, W, 80)
      ctx.strokeStyle = C + '0.2)'; ctx.lineWidth = 1
      ctx.beginPath(); ctx.moveTo(0, scanY); ctx.lineTo(W, scanY); ctx.stroke()

      // Outer rings
      ctx.strokeStyle = C + '0.1)'; ctx.lineWidth = 1
      ctx.beginPath(); ctx.arc(cx, cy, Math.min(W,H)*0.36, 0, Math.PI*2); ctx.stroke()
      ctx.strokeStyle = C + '0.05)'
      ctx.beginPath(); ctx.arc(cx, cy, Math.min(W,H)*0.44, 0, Math.PI*2); ctx.stroke()

      // Rotating arc
      const a = frame * 0.007
      ctx.strokeStyle = C + '0.5)'; ctx.lineWidth = 1.5
      ctx.beginPath(); ctx.arc(cx, cy, Math.min(W,H)*0.36, a, a + 0.7); ctx.stroke()
      ctx.beginPath(); ctx.arc(cx, cy, Math.min(W,H)*0.36, a + Math.PI, a + Math.PI + 0.7); ctx.stroke()

      // Connections
      outer.forEach((n, i) => {
        outer.slice(i+1).forEach(m => {
          const d = Math.hypot(n.x-m.x, n.y-m.y)
          if (d < 160) {
            ctx.strokeStyle = C + (((160-d)/160)*0.12) + ')'
            ctx.lineWidth = 0.5
            ctx.beginPath(); ctx.moveTo(n.x,n.y); ctx.lineTo(m.x,m.y); ctx.stroke()
          }
        })
        inner.forEach(m => {
          const d = Math.hypot(n.x-m.x, n.y-m.y)
          if (d < 120) {
            ctx.strokeStyle = G + (((120-d)/120)*0.1) + ')'
            ctx.lineWidth = 0.5
            ctx.beginPath(); ctx.moveTo(n.x,n.y); ctx.lineTo(m.x,m.y); ctx.stroke()
          }
        })
      })

      // Packets + trails
      for (let i = packets.length - 1; i >= 0; i--) {
        const p = packets[i]
        p.t += p.speed
        if (p.t >= 1) { packets.splice(i, 1); continue }
        const px = p.from.x + (p.to.x - p.from.x) * p.t
        const py = p.from.y + (p.to.y - p.from.y) * p.t
        for (let k = 0; k < 6; k++) {
          const tt = p.t - k * 0.012
          if (tt < 0) continue
          const tx = p.from.x + (p.to.x - p.from.x) * tt
          const ty = p.from.y + (p.to.y - p.from.y) * tt
          ctx.fillStyle = C + ((6-k)/6*0.7) + ')'
          ctx.beginPath(); ctx.arc(tx, ty, k === 0 ? 2.5 : 1.2, 0, Math.PI*2); ctx.fill()
        }
      }

      // Nodes
      const allNodes = [...outer, ...inner]
      allNodes.forEach(n => {
        n.x += n.vx; n.y += n.vy
        if (n.x < n.minX || n.x > n.maxX) n.vx *= -1
        if (n.y < n.minY || n.y > n.maxY) n.vy *= -1
        n.pulse += n.pulseSpeed
        const ps = n.size + Math.sin(n.pulse) * 1.2
        const isInner = inner.includes(n)
        const col = isInner ? G : C
        const grd = ctx.createRadialGradient(n.x,n.y,0, n.x,n.y,12)
        grd.addColorStop(0, col+'0.3)'); grd.addColorStop(1, col+'0)')
        ctx.fillStyle = grd
        ctx.beginPath(); ctx.arc(n.x,n.y,12,0,Math.PI*2); ctx.fill()
        ctx.fillStyle = col+'0.9)'
        ctx.beginPath(); ctx.arc(n.x,n.y,ps,0,Math.PI*2); ctx.fill()
      })

      // Target crosshair
      targetX += tdx; targetY += tdy
      if (targetX < 50 || targetX > W-50) tdx *= -1
      if (targetY < 50 || targetY > H-50) tdy *= -1
      const r2 = 22
      ctx.strokeStyle = C + '0.7)'; ctx.lineWidth = 1
      ctx.beginPath(); ctx.moveTo(targetX-r2,targetY); ctx.lineTo(targetX-7,targetY); ctx.stroke()
      ctx.beginPath(); ctx.moveTo(targetX+7,targetY); ctx.lineTo(targetX+r2,targetY); ctx.stroke()
      ctx.beginPath(); ctx.moveTo(targetX,targetY-r2); ctx.lineTo(targetX,targetY-7); ctx.stroke()
      ctx.beginPath(); ctx.moveTo(targetX,targetY+7); ctx.lineTo(targetX,targetY+r2); ctx.stroke()
      ;[[1,1],[1,-1],[-1,1],[-1,-1]].forEach(([sx,sy]) => {
        ctx.strokeStyle = C+'0.9)'; ctx.lineWidth = 1.5
        ctx.beginPath(); ctx.moveTo(targetX+sx*r2,targetY+sy*(r2-8)); ctx.lineTo(targetX+sx*r2,targetY+sy*r2); ctx.lineTo(targetX+sx*(r2-8),targetY+sy*r2); ctx.stroke()
      })
      ctx.fillStyle = C+'1)'; ctx.beginPath(); ctx.arc(targetX,targetY,2.5,0,Math.PI*2); ctx.fill()

      // HUD text
      ctx.fillStyle = C+'0.4)'; ctx.font = '9px JetBrains Mono, monospace'
      ctx.fillText('SYS.STATUS: ONLINE', 12, 22)
      ctx.fillText(`NODES: ${allNodes.length}`, 12, 36)
      ctx.fillText(`PKT: ${packets.length.toString().padStart(2,'0')}`, 12, 50)
      ctx.fillText(`F: ${frame.toString().padStart(6,'0')}`, 12, 64)

      frame++
      raf = requestAnimationFrame(draw)
    }

    draw()
    return () => { cancelAnimationFrame(raf); clearInterval(iv); ro.disconnect() }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full"
      style={{ display: 'block' }}
    />
  )
}
