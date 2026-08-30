"use client";

import { useRef } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { useReducedMotion } from "./useReducedMotion";

type MagneticButtonProps = {
  href?: string;
  onClick?: () => void;
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  className?: string;
  strength?: number;
  fullWidth?: boolean;
};

export function MagneticButton({
  href,
  onClick,
  children,
  variant = "primary",
  className,
  strength = 0.35,
  fullWidth = false,
}: MagneticButtonProps) {
  const ref = useRef<HTMLDivElement>(null);
  const reducedMotion = useReducedMotion();

  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const springX = useSpring(x, { stiffness: 250, damping: 20, mass: 0.4 });
  const springY = useSpring(y, { stiffness: 250, damping: 20, mass: 0.4 });

  function handleMouseMove(event: React.MouseEvent<HTMLDivElement>) {
    if (reducedMotion || !ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const relX = event.clientX - rect.left - rect.width / 2;
    const relY = event.clientY - rect.top - rect.height / 2;
    x.set(relX * strength);
    y.set(relY * strength);
  }

  function handleMouseLeave() {
    x.set(0);
    y.set(0);
  }

  const base =
    "relative inline-flex items-center justify-center gap-2 rounded-full px-7 py-3.5 text-sm font-semibold tracking-wide uppercase transition-colors duration-300 cursor-pointer select-none";

  const variants: Record<string, string> = {
    primary:
      "bg-foreground text-bg hover:bg-accent hover:text-white shadow-[0_1px_0_rgba(255,255,255,0.4)_inset]",
    secondary:
      "border border-border-strong text-foreground hover:border-accent hover:text-accent bg-white/[0.02]",
    ghost: "text-foreground/80 hover:text-accent",
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ x: springX, y: springY }}
      className={fullWidth ? "block w-full" : "inline-block"}
    >
      {href ? (
        <Link
          href={href}
          className={cn(base, variants[variant], fullWidth && "w-full", className)}
        >
          {children}
        </Link>
      ) : (
        <button
          type="button"
          onClick={onClick}
          className={cn(base, variants[variant], fullWidth && "w-full", className)}
        >
          {children}
        </button>
      )}
    </motion.div>
  );
}
