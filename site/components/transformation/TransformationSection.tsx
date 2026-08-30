"use client";

import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/ui/FadeIn";

const BEFORE = [
  "Missed calls",
  "Slow responses",
  "Manual follow-up",
  "Scattered tools",
  "Lost opportunities",
];

const AFTER = [
  "AI answers instantly",
  "Leads get followed up",
  "Appointments get booked",
  "Marketing works together",
  "Opportunities stay in the pipeline",
];

export function TransformationSection() {
  return (
    <section className="relative py-28 md:py-36">
      <Container>
        <SectionHeading
          eyebrow="The Shift"
          lines={["STOP CHASING LEADS.", "BUILD A SYSTEM THAT CHASES THEM."]}
          align="center"
          className="mx-auto max-w-3xl"
        />

        <div className="relative mt-16 grid grid-cols-1 gap-6 md:grid-cols-2 md:gap-0">
          <FadeIn className="md:pr-10">
            <div className="h-full rounded-3xl border border-border bg-white/[0.015] p-8 md:rounded-r-none">
              <span className="text-xs font-semibold uppercase tracking-[0.22em] text-muted-2">
                Before
              </span>
              <ul className="mt-6 flex flex-col gap-4">
                {BEFORE.map((item, i) => (
                  <motion.li
                    key={item}
                    initial={{ opacity: 0, x: -16 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, amount: 0.6 }}
                    transition={{ duration: 0.5, delay: i * 0.08 }}
                    className="flex items-center gap-3 text-[15px] text-muted"
                  >
                    <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-red-500/25 text-[11px] text-red-400/80">
                      &times;
                    </span>
                    {item}
                  </motion.li>
                ))}
              </ul>
            </div>
          </FadeIn>

          <div
            aria-hidden="true"
            className="absolute left-1/2 top-1/2 hidden h-14 w-14 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border border-border bg-bg text-accent md:flex"
          >
            <motion.svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              animate={{ x: [0, 4, 0] }}
              transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
            >
              <path d="M5 12h14" />
              <path d="M13 6l6 6-6 6" />
            </motion.svg>
          </div>

          <FadeIn delay={0.15} className="md:pl-10">
            <div className="h-full rounded-3xl border border-accent/25 bg-accent/[0.05] p-8 md:rounded-l-none">
              <span className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">
                After
              </span>
              <ul className="mt-6 flex flex-col gap-4">
                {AFTER.map((item, i) => (
                  <motion.li
                    key={item}
                    initial={{ opacity: 0, x: 16 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, amount: 0.6 }}
                    transition={{ duration: 0.5, delay: i * 0.08 }}
                    className="flex items-center gap-3 text-[15px] text-foreground/90"
                  >
                    <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-accent/40 text-[11px] text-accent">
                      &#10003;
                    </span>
                    {item}
                  </motion.li>
                ))}
              </ul>
            </div>
          </FadeIn>
        </div>
      </Container>
    </section>
  );
}
