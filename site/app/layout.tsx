import type { Metadata, Viewport } from "next";
import { Bricolage_Grotesque, Inter } from "next/font/google";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
  variable: "--font-bricolage",
  subsets: ["latin"],
  display: "swap",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const siteUrl = "https://mandaw1587-crypto.github.io/echorev-website";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "With Manny | AI Marketing Systems That Convert",
    template: "%s | With Manny",
  },
  description:
    "With Manny builds AI-powered marketing systems, websites, automation, and lead-generation solutions that help businesses attract, follow up with, and convert more customers.",
  keywords: [
    "AI marketing systems",
    "AI receptionist",
    "lead generation",
    "marketing automation",
    "websites that convert",
    "With Manny",
  ],
  authors: [{ name: "With Manny" }],
  openGraph: {
    title: "With Manny | AI Marketing Systems That Convert",
    description:
      "AI-powered marketing systems that help businesses attract leads, automate follow-up, and turn attention into revenue.",
    url: siteUrl,
    siteName: "With Manny",
    type: "website",
    images: [{ url: "/og.svg", width: 1200, height: 630, alt: "With Manny" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "With Manny | AI Marketing Systems That Convert",
    description:
      "AI-powered marketing systems that help businesses attract leads, automate follow-up, and turn attention into revenue.",
    images: ["/og.svg"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#08090c",
  colorScheme: "dark",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${bricolage.variable} ${inter.variable} h-full`}
    >
      <body className="min-h-full bg-bg text-foreground antialiased selection:bg-accent selection:text-white">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100] focus:rounded-md focus:bg-accent focus:px-4 focus:py-2 focus:text-white"
        >
          Skip to content
        </a>
        <div className="grain" aria-hidden="true" />
        {children}
      </body>
    </html>
  );
}
