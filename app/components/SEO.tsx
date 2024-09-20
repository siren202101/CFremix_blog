
import { MetaFunction } from "@remix-run/cloudflare";

interface SEOProps {
  title: string;
  description: string;
  image?: string;
  url: string;
}

export const SEO: MetaFunction = ({
  title,
  description,
  image,
  url,
}: SEOProps) => {
  return [
    { title },
    { name: "description", content: description },
    { property: "og:title", content: title },
    { property: "og:description", content: description },
    { property: "og:url", content: url },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: "summary_large_image" },
    { name: "twitter:title", content: title },
    { name: "twitter:description", content: description },
    ...(image
      ? [
          { property: "og:image", content: image },
          { name: "twitter:image", content: image },
        ]
      : []),
  ];
};
