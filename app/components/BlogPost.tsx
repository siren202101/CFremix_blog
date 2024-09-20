
import { Link } from "@remix-run/react";
import { useTranslation } from "react-i18next";
import SocialShare from "./SocialShare";

interface BlogPostProps {
  title: string;
  date: string;
  description: string;
  categories: string[];
  slug: string;
}

export default function BlogPost({
  title,
  date,
  description,
  categories,
  slug,
}: BlogPostProps) {
  const { t } = useTranslation();

  return (
    <article className="mb-8">
      <h2 className="text-2xl font-bold mb-2">
        <Link to={`/posts/${slug}`} className="hover:underline">
          {title}
        </Link>
      </h2>
      <p className="text-gray-500 mb-2">{date}</p>
      <p className="mb-2">{description}</p>
      <div className="flex space-x-2 mb-2">
        {categories.map((category) => (
          <span
            key={category}
            className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded text-sm"
          >
            {category}
          </span>
        ))}
      </div>
      <SocialShare title={title} url={`/posts/${slug}`} />
    </article>
  );
}
