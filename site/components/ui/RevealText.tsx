"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { cn } from "@/lib/utils";

type RevealTextProps = {
  lines: string[];
  as?: "h1" | "h2" | "h3";
  className?: string;
  lineClassName?: string;
  delay?: number;
  once?: boolean;
};

export function RevealText({
  lines,
  as = "h2",
  className,
  lineClassName,
  delay = 0,
  once = true,
}: RevealTextProps) {
  const Tag = as;
  // The animated element sits inside an `overflow-hidden` mask and starts
  // translated below that mask's bounds, so it is always clipped to zero
  // area — observing it directly with `whileInView` never intersects.
  // Watch the unclipped heading instead and drive the reveal from that.
  const ref = useRef<HTMLHeadingElement>(null);
  const inView = useInView(ref, { once, amount: 0.5 });

  return (
    <Tag ref={ref} className={cn("flex flex-col", className)}>
      {lines.map((line, i) => (
        <span key={line} className="overflow-hidden">
          <motion.span
            initial={{ y: "110%", opacity: 0 }}
            animate={inView ? { y: "0%", opacity: 1 } : undefined}
            transition={{
              duration: 0.9,
              delay: delay + i * 0.09,
              ease: [0.16, 1, 0.3, 1],
            }}
            className={cn("block", lineClassName)}
          >
            {line}
          </motion.span>
        </span>
      ))}
    </Tag>
  );
}
