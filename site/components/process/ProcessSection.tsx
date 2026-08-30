import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/ui/FadeIn";

const STEPS = [
  {
    number: "01",
    title: "Discover",
    description:
      "We identify where your current marketing system is leaking opportunities.",
  },
  {
    number: "02",
    title: "Design",
    description:
      "We design the website, funnel, automation, and customer journey.",
  },
  {
    number: "03",
    title: "Build",
    description:
      "We connect the AI, marketing, automation, and conversion systems.",
  },
  {
    number: "04",
    title: "Launch",
    description: "We launch, measure, refine, and improve the system.",
  },
];

export function ProcessSection() {
  return (
    <section className="relative py-28 md:py-36">
      <Container>
        <SectionHeading eyebrow="Process" lines={["BUILT TO MOVE FAST."]} />

        <div className="relative mt-16">
          <div
            aria-hidden="true"
            className="absolute left-6 top-2 hidden h-[calc(100%-1rem)] w-px bg-border md:left-0 md:right-0 md:top-6 md:h-px md:w-full"
          />
          <div className="grid grid-cols-1 gap-10 md:grid-cols-4 md:gap-8">
            {STEPS.map((step, i) => (
              <FadeIn key={step.number} delay={i * 0.1}>
                <div className="relative flex gap-5 pl-0 md:flex-col md:gap-6">
                  <div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-border-strong bg-bg font-display text-sm font-bold text-accent">
                    {step.number}
                  </div>
                  <div>
                    <h3 className="font-display text-xl font-semibold text-foreground">
                      {step.title}
                    </h3>
                    <p className="mt-2 max-w-xs text-[15px] leading-relaxed text-muted">
                      {step.description}
                    </p>
                  </div>
                </div>
              </FadeIn>
            ))}
          </div>
        </div>
      </Container>
    </section>
  );
}
