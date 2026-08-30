"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform, type MotionValue } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { cn } from "@/lib/utils";

const BROKEN_STEPS = ["Traffic", "Lead", "Wait", "Lost Customer"];
const FIXED_STEPS = ["Traffic", "AI", "Follow-Up", "Appointment", "Customer"];

export function ProblemSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end end"],
  });

  const brokenOpacity = useTransform(scrollYProgress, [0.15, 0.4], [1, 0]);
  const brokenY = useTransform(scrollYProgress, [0.15, 0.4], [0, -20]);
  const fixedOpacity = useTransform(scrollYProgress, [0.45, 0.7], [0, 1]);
  const fixedY = useTransform(scrollYProgress, [0.45, 0.7], [20, 0]);
  const strike = useTransform(scrollYProgress, [0.05, 0.35], [0, 1]);

  return (
    <section ref={sectionRef} id="problem" className="relative h-[220vh]">
      <div className="sticky top-0 flex h-screen flex-col justify-center overflow-hidden py-20">
        <Container>
          <SectionHeading
            eyebrow="The Problem"
            lines={["YOUR MARKETING ISN'T THE PROBLEM.", "YOUR SYSTEM IS."]}
            description="Most businesses spend money generating attention, then lose potential customers because the follow-up is slow, fragmented, or completely manual."
          />
        </Container>

        {/* Both rows occupy the same grid cell so the container always
            sizes to whichever is tallest, keeping the crossfade legible
            on narrow screens instead of the two stacks bleeding together. */}
        <div className="relative mt-16 grid">
          <motion.div
            style={{ opacity: brokenOpacity, y: brokenY }}
            className="col-start-1 row-start-1"
          >
            <Container>
              <FlowRow steps={BROKEN_STEPS} broken strikeProgress={strike} />
            </Container>
          </motion.div>

          <motion.div
            style={{ opacity: fixedOpacity, y: fixedY }}
            className="col-start-1 row-start-1"
          >
            <Container>
              <FlowRow steps={FIXED_STEPS} />
            </Container>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function FlowRow({
  steps,
  broken = false,
  strikeProgress,
}: {
  steps: string[];
  broken?: boolean;
  strikeProgress?: MotionValue<number>;
}) {
  return (
    <div className="-mx-5 flex items-center gap-3 overflow-x-auto px-5 pb-2 sm:gap-4 md:justify-between md:overflow-visible">
      {steps.map((step, i) => (
        <div key={step} className="flex shrink-0 items-center gap-3 sm:gap-4">
          <div
            className={cn(
              "relative flex min-w-[104px] items-center justify-center rounded-2xl border px-4 py-4 text-center text-xs font-semibold uppercase tracking-wide sm:min-w-[130px] sm:px-5 sm:py-5 sm:text-sm",
              broken
                ? i === steps.length - 1
                  ? "border-red-500/30 bg-red-500/[0.06] text-red-300"
                  : "border-border bg-white/[0.02] text-muted"
                : "border-accent/30 bg-accent/[0.08] text-foreground"
            )}
          >
            {step}
            {broken && (
              <motion.span
                style={{ scaleX: strikeProgress }}
                className="absolute left-0 right-0 top-1/2 h-px origin-left bg-red-400/70"
              />
            )}
          </div>
          {i < steps.length - 1 && (
            <span
              aria-hidden="true"
              className={cn(
                "shrink-0 text-base sm:text-lg",
                broken ? "text-muted/40" : "text-accent/60"
              )}
            >
              &rarr;
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
