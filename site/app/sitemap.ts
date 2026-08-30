import type { MetadataRoute } from "next";

const siteUrl = "https://mandaw1587-crypto.github.io/echorev-website";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: siteUrl,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 1,
    },
  ];
}
