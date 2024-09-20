
import { useState } from "react";
import { Link } from "@remix-run/react";
import { useTranslation } from "react-i18next";

interface SearchProps {
  posts: Array<{
    slug: string;
    title: string;
    description: string;
  }>;
}

export default function Search({ posts }: SearchProps) {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState("");

  const filteredPosts = posts.filter(
    (post) =>
      post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      post.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder={t("searchPosts")}
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full p-2 border rounded mb-4"
      />
      {searchTerm && (
        <ul>
          {filteredPosts.map((post) => (
            <li key={post.slug} className="mb-2">
              <Link to={`/posts/${post.slug}`} className="hover:underline">
                {post.title}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
