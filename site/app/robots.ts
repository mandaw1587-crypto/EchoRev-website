import type { MetadataRoute } from "next";

const siteUrl = "https://mandaw1587-crypto.github.io/echorev-website";

export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
    },
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
