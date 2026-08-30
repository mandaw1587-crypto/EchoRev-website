"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/ui/FadeIn";
import { useReducedMotion } from "@/components/ui/useReducedMotion";
import { cn } from "@/lib/utils";

const STAGES = [
  {
    number: "01",
    title: "Attract",
    summary: "Get the right people to discover the business.",
    detail:
      "Get the right people to discover the business through content, search, and paid placement built around what your customers actually search for.",
  },
  {
    number: "02",
    title: "Capture",
    summary: "Turn attention into identifiable leads.",
    detail:
      "Turn attention into identifiable leads with landing pages and forms engineered to convert visitors before they leave.",
  },
  {
    number: "03",
    title: "Follow Up",
    summary: "Use AI to respond instantly and consistently.",
    detail:
      "Use AI to respond instantly and consistently, every time, so no lead waits and no opportunity goes cold.",
  },
  {
    number: "04",
    title: "Convert",
    summary: "Turn qualified leads into customers.",
    detail:
      "Turn qualified leads into conversations, appointments, and customers with a follow-through system that never drops the ball.",
  },
];

export function SystemSection() {
  const [active, setActive] = useState(0);
  const reducedMotion = useReducedMotion();

  return (
    <section id="system" className="relative py-28 md:py-36">
      <Container>
        <SectionHeading
          eyebrow="The Framework"
          lines={["THE WITH MANNY SYSTEM"]}
          description="From first impression to booked customer."
        />

        <div className="relative mt-20">
          <div
            aria-hidden="true"
            className="absolute left-0 right-0 top-8 hidden h-px bg-gradient-to-r from-transparent via-border-strong to-transparent md:block"
          >
            {!reducedMotion && (
              <motion.span
                className="absolute top-1/2 h-2 w-2 -translate-y-1/2 rounded-full bg-accent shadow-[0_0_14px_3px_rgba(59,123,255,0.7)]"
                animate={{ left: ["0%", "100%"] }}
                transition={{ duration: 5, repeat: Infinity, ease: "linear" }}
              />
            )}
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-4 md:gap-8">
            {STAGES.map((stage, i) => (
              <FadeIn key={stage.title} delay={i * 0.1}>
                <button
                  type="button"
                  onMouseEnter={() => setActive(i)}
                  onFocus={() => setActive(i)}
                  onClick={() => setActive(i)}
                  aria-pressed={active === i}
                  className={cn(
                    "group flex w-full flex-col items-start gap-4 rounded-2xl border p-6 text-left transition-all duration-300",
                    active === i
                      ? "border-accent/50 bg-accent/[0.06]"
                      : "border-border bg-white/[0.01] hover:border-border-strong"
                  )}
                >
                  <span
                    className={cn(
                      "relative z-10 flex h-8 w-8 items-center justify-center rounded-full border text-xs font-bold transition-colors duration-300 md:mx-auto",
                      active === i
                        ? "border-accent bg-accent text-white"
                        : "border-border-strong text-muted"
                    )}
                  >
                    {stage.number}
                  </span>
                  <div className="md:text-center">
                    <h3 className="font-display text-xl font-semibold text-foreground">
                      {stage.title}
                    </h3>
                    <p className="mt-1 text-sm text-muted">{stage.summary}</p>
                  </div>
                </button>
              </FadeIn>
            ))}
          </div>

          <div className="relative mt-10 min-h-[92px] overflow-hidden rounded-2xl border border-border bg-surface px-8 py-7">
            <AnimatePresence mode="wait">
              <motion.p
                key={active}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                className="text-lg leading-relaxed text-foreground/90"
              >
                <span className="mr-2 font-display font-semibold text-accent">
                  {STAGES[active].number}
                </span>
                {STAGES[active].detail}
              </motion.p>
            </AnimatePresence>
          </div>
        </div>
      </Container>
    </section>
  );
}
