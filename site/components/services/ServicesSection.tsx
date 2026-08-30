import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/ui/FadeIn";
import { ServiceCard } from "./ServiceCard";
import { ContentIcon, LeadGenIcon, ReceptionistIcon, WebsiteIcon } from "./icons";

const SERVICES = [
  {
    index: "01",
    title: "AI Receptionist",
    description:
      "AI-powered voice and text agents that answer questions, qualify leads, book appointments, and follow up 24/7.",
    icon: <ReceptionistIcon />,
  },
  {
    index: "02",
    title: "Lead Generation",
    description:
      "Landing pages, funnels, forms, and acquisition systems designed to turn attention into qualified leads.",
    icon: <LeadGenIcon />,
  },
  {
    index: "03",
    title: "AI Content Systems",
    description:
      "Strategic content systems that help businesses stay visible without manually creating every piece of content.",
    icon: <ContentIcon />,
  },
  {
    index: "04",
    title: "Websites That Convert",
    description:
      "Premium websites and landing pages designed around user experience, credibility, and conversion.",
    icon: <WebsiteIcon />,
  },
];

export function ServicesSection() {
  return (
    <section id="services" className="relative py-28 md:py-36">
      <Container>
        <SectionHeading
          eyebrow="Services"
          lines={["ONE SYSTEM.", "EVERYTHING CONNECTED."]}
        />

        <div className="mt-16 grid grid-cols-1 gap-5 md:grid-cols-2">
          {SERVICES.map((service, i) => (
            <FadeIn key={service.title} delay={i * 0.08}>
              <ServiceCard {...service} />
            </FadeIn>
          ))}
        </div>
      </Container>
    </section>
  );
}
