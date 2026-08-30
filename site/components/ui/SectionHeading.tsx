import { cn } from "@/lib/utils";
import { RevealText } from "./RevealText";
import { FadeIn } from "./FadeIn";

type SectionHeadingProps = {
  eyebrow?: string;
  lines: string[];
  description?: string;
  align?: "left" | "center";
  as?: "h1" | "h2" | "h3";
  className?: string;
};

export function SectionHeading({
  eyebrow,
  lines,
  description,
  align = "left",
  as = "h2",
  className,
}: SectionHeadingProps) {
  return (
    <div
      className={cn(
        "flex flex-col gap-5",
        align === "center" && "items-center text-center",
        className
      )}
    >
      {eyebrow && (
        <FadeIn y={12}>
          <span className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-accent">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" aria-hidden="true" />
            {eyebrow}
          </span>
        </FadeIn>
      )}
      <RevealText
        as={as}
        lines={lines}
        className={cn(
          "font-display text-[clamp(2rem,5vw,3.75rem)] font-semibold leading-[1.05] tracking-tight text-balance",
          align === "center" && "items-center"
        )}
      />
      {description && (
        <FadeIn delay={0.15} y={16}>
          <p
            className={cn(
              "max-w-2xl text-lg leading-relaxed text-muted",
              align === "center" && "mx-auto"
            )}
          >
            {description}
          </p>
        </FadeIn>
      )}
    </div>
  );
}
