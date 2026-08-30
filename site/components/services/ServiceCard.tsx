"use client";

import { useRef } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useReducedMotion } from "@/components/ui/useReducedMotion";

type ServiceCardProps = {
  index: string;
  title: string;
  description: string;
  icon: React.ReactNode;
};

export function ServiceCard({ index, title, description, icon }: ServiceCardProps) {
  const ref = useRef<HTMLDivElement>(null);
  const reducedMotion = useReducedMotion();

  const rotateX = useMotionValue(0);
  const rotateY = useMotionValue(0);
  const springRotateX = useSpring(rotateX, { stiffness: 200, damping: 22 });
  const springRotateY = useSpring(rotateY, { stiffness: 200, damping: 22 });

  const glowX = useMotionValue(50);
  const glowY = useMotionValue(50);

  function handleMouseMove(event: React.MouseEvent<HTMLDivElement>) {
    if (reducedMotion || !ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const px = (event.clientX - rect.left) / rect.width;
    const py = (event.clientY - rect.top) / rect.height;
    rotateY.set((px - 0.5) * 10);
    rotateX.set((0.5 - py) * 10);
    glowX.set(px * 100);
    glowY.set(py * 100);
  }

  function handleMouseLeave() {
    rotateX.set(0);
    rotateY.set(0);
  }

  const background = useTransform(
    [glowX, glowY],
    ([x, y]) =>
      `radial-gradient(320px circle at ${x}% ${y}%, rgba(59,123,255,0.16), transparent 65%)`
  );

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        rotateX: springRotateX,
        rotateY: springRotateY,
        transformPerspective: 900,
      }}
      className="group relative overflow-hidden rounded-3xl border border-border bg-surface p-8 transition-colors duration-300 hover:border-accent/40"
    >
      <motion.div
        aria-hidden="true"
        style={{ background }}
        className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100"
      />

      <div className="relative flex items-start justify-between">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-border-strong bg-white/[0.03] text-accent transition-transform duration-500 group-hover:-translate-y-1 group-hover:scale-105">
          {icon}
        </div>
        <span className="font-display text-sm font-semibold text-muted-2">{index}</span>
      </div>

      <h3 className="relative mt-8 font-display text-2xl font-semibold tracking-tight text-foreground transition-transform duration-500 group-hover:translate-x-1">
        {title}
      </h3>
      <p className="relative mt-3 text-[15px] leading-relaxed text-muted">
        {description}
      </p>

      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-3xl opacity-0 transition-opacity duration-500 group-hover:opacity-100"
        style={{
          boxShadow: "inset 0 0 0 1px rgba(59,123,255,0.35)",
        }}
      />
    </motion.div>
  );
}
