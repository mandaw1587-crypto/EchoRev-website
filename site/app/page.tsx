import { Navbar } from "@/components/navigation/Navbar";
import { Hero } from "@/components/hero/Hero";
import { ProblemSection } from "@/components/problem/ProblemSection";
import { ServicesSection } from "@/components/services/ServicesSection";
import { SystemSection } from "@/components/system/SystemSection";
import { TransformationSection } from "@/components/transformation/TransformationSection";
import { ProcessSection } from "@/components/process/ProcessSection";
import { AboutSection } from "@/components/about/AboutSection";
import { CTASection } from "@/components/cta/CTASection";
import { Footer } from "@/components/footer/Footer";

export default function Home() {
  return (
    <>
      <Navbar />
      <main id="main-content">
        <Hero />
        <ProblemSection />
        <ServicesSection />
        <SystemSection />
        <TransformationSection />
        <ProcessSection />
        <AboutSection />
        <CTASection />
      </main>
      <Footer />
    </>
  );
}
