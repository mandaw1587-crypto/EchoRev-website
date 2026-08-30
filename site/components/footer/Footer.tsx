import Link from "next/link";
import { Container } from "@/components/ui/Container";

const FOOTER_LINKS = [
  { label: "Services", href: "#services" },
  { label: "How It Works", href: "#system" },
  { label: "About", href: "#about" },
  { label: "Contact", href: "#contact" },
];

const SOCIAL_LINKS = [
  { label: "Instagram", href: "#" },
  { label: "LinkedIn", href: "#" },
  { label: "YouTube", href: "#" },
];

export function Footer() {
  return (
    <footer className="relative border-t border-border">
      <Container className="flex flex-col gap-12 py-16">
        <div className="flex flex-col justify-between gap-10 md:flex-row md:items-start">
          <div>
            <span className="font-display text-xl font-bold tracking-tight text-foreground">
              WITH<span className="text-accent">&nbsp;MANNY</span>
            </span>
            <p className="mt-3 text-sm uppercase tracking-[0.2em] text-muted-2">
              AI &amp; Business Strategies
            </p>
          </div>

          <nav
            className="flex flex-wrap gap-x-8 gap-y-3 text-sm text-muted"
            aria-label="Footer"
          >
            {FOOTER_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="transition-colors hover:text-foreground"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="flex gap-6 text-sm text-muted">
            {SOCIAL_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="transition-colors hover:text-foreground"
              >
                {link.label}
              </a>
            ))}
          </div>
        </div>

        <div className="flex flex-col-reverse gap-4 border-t border-border pt-8 text-xs text-muted-2 md:flex-row md:items-center md:justify-between">
          <p>&copy; 2026 With Manny. All rights reserved.</p>
          <p>Marketing, rebuilt with AI.</p>
        </div>
      </Container>
    </footer>
  );
}
