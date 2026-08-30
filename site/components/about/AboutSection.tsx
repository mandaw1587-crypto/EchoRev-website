import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/ui/FadeIn";

export function AboutSection() {
  return (
    <section id="about" className="relative py-28 md:py-36">
      <Container>
        <div className="grid grid-cols-1 items-start gap-12 md:grid-cols-2 md:gap-20">
          <SectionHeading
            eyebrow="About With Manny"
            lines={["TECHNOLOGY SHOULD MAKE", "BUSINESS SIMPLER."]}
          />
          <FadeIn delay={0.15}>
            <div className="flex flex-col gap-6 text-lg leading-relaxed text-muted">
              <p>
                With Manny helps businesses turn complicated marketing and AI
                technology into simple systems that actually work.
              </p>
              <p>
                No bolted-on tools. No manual follow-up. Just a connected
                system that attracts the right people, responds instantly, and
                turns that attention into customers.
              </p>
            </div>
          </FadeIn>
        </div>
      </Container>
    </section>
  );
}
