"use client";

import { useEffect, useRef } from "react";
import { useReducedMotion } from "@/components/ui/useReducedMotion";

type Particle = {
  theta: number;
  phi: number;
  radius: number;
  size: number;
};

function makeParticles(count: number): Particle[] {
  const particles: Particle[] = [];
  for (let i = 0; i < count; i++) {
    particles.push({
      theta: Math.random() * Math.PI * 2,
      phi: Math.acos(2 * Math.random() - 1),
      radius: 1 + Math.random() * 0.55,
      size: 0.6 + Math.random() * 1.6,
    });
  }
  return particles;
}

export function HeroVisual() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    const canvasEl = canvasRef.current;
    const wrapperEl = wrapperRef.current;
    if (!canvasEl || !wrapperEl) return;
    const ctxEl = canvasEl.getContext("2d");
    if (!ctxEl) return;

    const canvas: HTMLCanvasElement = canvasEl;
    const wrapper: HTMLDivElement = wrapperEl;
    const ctx: CanvasRenderingContext2D = ctxEl;

    let width = 0;
    let height = 0;
    let dpr = Math.min(window.devicePixelRatio || 1, 2);
    const particles = makeParticles(width > 900 ? 140 : 90);

    let rotationY = 0;
    let rotationX = 0.35;
    let targetTiltX = 0;
    let targetTiltY = 0;
    let scrollProgress = 0;
    let visible = true;
    let rafId = 0;

    function resize() {
      width = wrapper.clientWidth;
      height = wrapper.clientHeight;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    // Measure scroll progress from the enclosing section, not this wrapper:
    // the wrapper is intentionally offset (top/right -10%) for layout, so
    // its own rect is never at 0 even at the very top of the page.
    const progressEl = wrapper.closest("section") ?? wrapper;

    function onScroll() {
      const rect = progressEl.getBoundingClientRect();
      const progress = -rect.top / window.innerHeight;
      scrollProgress = Math.min(Math.max(progress, 0), 1.6);
    }

    function onPointerMove(event: PointerEvent) {
      const rect = wrapper.getBoundingClientRect();
      const relX = (event.clientX - rect.left - rect.width / 2) / rect.width;
      const relY = (event.clientY - rect.top - rect.height / 2) / rect.height;
      targetTiltY = relX * 0.6;
      targetTiltX = 0.35 - relY * 0.35;
    }

    function drawStatic() {
      resize();
      ctx.clearRect(0, 0, width, height);
      drawScene(0.35, 0, 1);
    }

    function drawScene(rotX: number, rotY: number, scale: number) {
      const cx = width / 2;
      const cy = height / 2;
      const baseRadius = Math.min(width, height) * 0.3 * scale;
      const focal = baseRadius * 2.4;

      const orbGradient = ctx.createRadialGradient(
        cx - baseRadius * 0.35,
        cy - baseRadius * 0.4,
        baseRadius * 0.05,
        cx,
        cy,
        baseRadius * 1.05
      );
      orbGradient.addColorStop(0, "rgba(150, 180, 255, 0.55)");
      orbGradient.addColorStop(0.35, "rgba(59, 123, 255, 0.28)");
      orbGradient.addColorStop(0.7, "rgba(20, 30, 55, 0.18)");
      orbGradient.addColorStop(1, "rgba(8, 9, 12, 0)");
      ctx.beginPath();
      ctx.fillStyle = orbGradient;
      ctx.arc(cx, cy, baseRadius * 1.05, 0, Math.PI * 2);
      ctx.fill();

      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, baseRadius * 0.62, 0, Math.PI * 2);
      const glassGradient = ctx.createLinearGradient(
        cx - baseRadius,
        cy - baseRadius,
        cx + baseRadius,
        cy + baseRadius
      );
      glassGradient.addColorStop(0, "rgba(255,255,255,0.10)");
      glassGradient.addColorStop(0.45, "rgba(59,123,255,0.10)");
      glassGradient.addColorStop(1, "rgba(123,107,255,0.06)");
      ctx.fillStyle = glassGradient;
      ctx.fill();
      ctx.lineWidth = 1;
      ctx.strokeStyle = "rgba(160,190,255,0.25)";
      ctx.stroke();
      ctx.restore();

      const projected = particles.map((p) => {
        const sx = p.radius * baseRadius * Math.sin(p.phi) * Math.cos(p.theta + rotY);
        const sy = p.radius * baseRadius * Math.cos(p.phi);
        const sz = p.radius * baseRadius * Math.sin(p.phi) * Math.sin(p.theta + rotY);

        const cosX = Math.cos(rotX);
        const sinX = Math.sin(rotX);
        const y2 = sy * cosX - sz * sinX;
        const z2 = sy * sinX + sz * cosX;

        const perspective = focal / (focal + z2);
        return {
          x: cx + sx * perspective,
          y: cy + y2 * perspective,
          z: z2,
          size: p.size * perspective,
        };
      });

      projected.sort((a, b) => a.z - b.z);

      for (let i = 0; i < projected.length; i++) {
        for (let j = i + 1; j < projected.length; j++) {
          const a = projected[i];
          const b = projected[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < baseRadius * 0.32) {
            const alpha = (1 - dist / (baseRadius * 0.32)) * 0.18;
            ctx.strokeStyle = `rgba(120,160,255,${alpha})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      for (const p of projected) {
        const depthAlpha = 0.35 + ((p.z / baseRadius) * 0.5 + 0.5) * 0.5;
        ctx.beginPath();
        ctx.fillStyle = `rgba(210,225,255,${Math.min(depthAlpha, 0.9)})`;
        ctx.arc(p.x, p.y, Math.max(p.size, 0.4), 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.beginPath();
      const rim = ctx.createRadialGradient(
        cx,
        cy,
        baseRadius * 0.9,
        cx,
        cy,
        baseRadius * 1.15
      );
      rim.addColorStop(0, "rgba(59,123,255,0)");
      rim.addColorStop(1, "rgba(59,123,255,0.16)");
      ctx.fillStyle = rim;
      ctx.arc(cx, cy, baseRadius * 1.15, 0, Math.PI * 2);
      ctx.fill();
    }

    if (reducedMotion) {
      drawStatic();
      window.addEventListener("resize", drawStatic);
      return () => window.removeEventListener("resize", drawStatic);
    }

    resize();

    const observer = new IntersectionObserver(
      ([entry]) => {
        visible = entry.isIntersecting;
      },
      { threshold: 0 }
    );
    observer.observe(wrapper);

    function tick() {
      rafId = requestAnimationFrame(tick);
      if (!visible) return;
      rotationY += 0.0016;
      rotationX += (targetTiltX - rotationX) * 0.04;
      const lerpedRotY = rotationY + (targetTiltY - 0) * 0.001 * 40;
      ctx.clearRect(0, 0, width, height);
      const scale = 1 - Math.min(scrollProgress, 1) * 0.18;
      ctx.save();
      ctx.translate(0, -scrollProgress * height * 0.12);
      ctx.globalAlpha = Math.max(1 - scrollProgress * 0.9, 0);
      drawScene(rotationX, lerpedRotY, scale);
      ctx.restore();
    }

    window.addEventListener("resize", resize);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("pointermove", onPointerMove);
    onScroll();
    tick();

    return () => {
      cancelAnimationFrame(rafId);
      observer.disconnect();
      window.removeEventListener("resize", resize);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("pointermove", onPointerMove);
    };
  }, [reducedMotion]);

  return (
    <div ref={wrapperRef} className="absolute inset-0" aria-hidden="true">
      <canvas ref={canvasRef} className="h-full w-full" />
    </div>
  );
}
