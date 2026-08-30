import { Container } from "@/components/ui/Container";
import { RevealText } from "@/components/ui/RevealText";
import { FadeIn } from "@/components/ui/FadeIn";
import { MagneticButton } from "@/components/ui/MagneticButton";

export function CTASection() {
  return (
    <section id="contact" className="relative overflow-hidden py-32 md:py-44">
      <div aria-hidden="true" className="absolute inset-0 -z-10">
        <div className="absolute left-1/2 top-1/2 h-[600px] w-[900px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-accent/[0.14] blur-[120px] motion-safe:animate-pulse" />
        <div className="absolute left-[20%] top-[70%] h-[380px] w-[380px] rounded-full bg-accent-2/[0.12] blur-[110px]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,var(--color-bg)_75%)]" />
      </div>

      <Container className="text-center">
        <div className="mx-auto flex max-w-2xl flex-col items-center">
          <RevealText
            as="h2"
            lines={["READY TO BUILD YOUR", "MARKETING SYSTEM?"]}
            className="items-center font-display text-[clamp(2.25rem,6vw,4.25rem)] font-semibold leading-[1.04] tracking-tight text-foreground"
          />
          <FadeIn delay={0.2}>
            <p className="mt-7 text-lg leading-relaxed text-muted">
              Let&apos;s turn your website, marketing, and AI tools into one
              system designed to generate and convert opportunities.
            </p>
          </FadeIn>
          <FadeIn delay={0.35}>
            <div className="mt-10 flex flex-col gap-4 sm:flex-row">
              <MagneticButton
                href="mailto:hello@withmanny.com?subject=Strategy%20Call%20Request"
                variant="primary"
              >
                Book a Strategy Call
              </MagneticButton>
              <MagneticButton href="#services" variant="secondary">
                Explore Services
              </MagneticButton>
            </div>
          </FadeIn>
        </div>
      </Container>
    </section>
  );
}
