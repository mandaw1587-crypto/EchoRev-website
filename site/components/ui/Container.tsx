import { cn } from "@/lib/utils";

export function Container({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={cn("container-px mx-auto w-full max-w-[1400px]", className)}>
      {children}
    </div>
  );
}
