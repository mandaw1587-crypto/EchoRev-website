"use client";

import { useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion, useMotionValueEvent, useScroll } from "framer-motion";
import { cn } from "@/lib/utils";
import { MagneticButton } from "@/components/ui/MagneticButton";

const NAV_LINKS = [
  { label: "Services", href: "#services" },
  { label: "How It Works", href: "#system" },
  { label: "About", href: "#about" },
  { label: "Contact", href: "#contact" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const { scrollY } = useScroll();

  useMotionValueEvent(scrollY, "change", (latest) => {
    setScrolled(latest > 24);
  });

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <div
        className={cn(
          "mx-auto transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
          scrolled ? "max-w-[1100px] mt-3" : "max-w-[1400px] mt-0"
        )}
      >
        <div
          className={cn(
            "container-px flex items-center justify-between border-b transition-all duration-500",
            scrolled
              ? "h-16 rounded-full border-border bg-bg/70 backdrop-blur-xl shadow-[0_8px_40px_-12px_rgba(0,0,0,0.6)] mx-4 sm:mx-6"
              : "h-20 border-transparent bg-transparent"
          )}
        >
          <Link
            href="#top"
            className="font-display text-lg font-bold tracking-tight text-foreground"
          >
            WITH<span className="text-accent">&nbsp;MANNY</span>
          </Link>

          <nav className="hidden items-center gap-9 md:flex" aria-label="Primary">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm font-medium text-muted transition-colors duration-200 hover:text-foreground"
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="hidden md:block">
            <MagneticButton href="#contact" variant="primary" className="px-5 py-2.5 text-xs">
              Book a Strategy Call
            </MagneticButton>
          </div>

          <button
            type="button"
            className="flex h-10 w-10 items-center justify-center rounded-full border border-border text-foreground md:hidden"
            aria-label={menuOpen ? "Close menu" : "Open menu"}
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <div className="relative h-3.5 w-4">
              <span
                className={cn(
                  "absolute left-0 top-0 h-[1.5px] w-4 bg-foreground transition-transform duration-300",
                  menuOpen && "translate-y-[6.5px] rotate-45"
                )}
              />
              <span
                className={cn(
                  "absolute left-0 bottom-0 h-[1.5px] w-4 bg-foreground transition-transform duration-300",
                  menuOpen && "-translate-y-[6.5px] -rotate-45"
                )}
              />
            </div>
          </button>
        </div>
      </div>

      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="mx-4 mt-2 rounded-3xl border border-border bg-bg-elevated/95 backdrop-blur-xl md:hidden"
          >
            <nav className="flex flex-col gap-1 p-4" aria-label="Mobile">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMenuOpen(false)}
                  className="rounded-xl px-4 py-3 text-base font-medium text-foreground/90 transition-colors hover:bg-white/5"
                >
                  {link.label}
                </Link>
              ))}
              <div className="p-2 pt-3">
                <MagneticButton
                  href="#contact"
                  variant="primary"
                  fullWidth
                  strength={0}
                >
                  Book a Strategy Call
                </MagneticButton>
              </div>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
