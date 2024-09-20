import os
import json

def create_file(file_path, content):
    """Creates a file with the given content.

    Args:
        file_path (str): The path to the file to create.
        content (str): The content to write to the file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"生成 {file_path} 文件成功")

# Define file paths and content
files = {
    "blog/package.json": """
{
  "name": "blog",
  "private": true,
  "sideEffects": false,
  "type": "module",
  "scripts": {
    "build": "remix build",
    "dev": "remix dev --manual",
    "start": "remix-serve ./build/index.js",
    "typecheck": "tsc"
  },
  "dependencies": {
    "@remix-run/cloudflare": "^2.0.0",
    "@remix-run/cloudflare-pages": "^2.0.0",
    "@remix-run/css-bundle": "^2.0.0",
    "@remix-run/react": "^2.0.0",
    "@remix-run/serve": "^2.0.0",
    "isbot": "^3.6.8",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "remix-i18next": "^5.3.0",
    "i18next": "^23.4.4",
    "react-i18next": "^13.1.2",
    "gray-matter": "^4.0.3",
    "remark": "^14.0.3",
    "remark-html": "^15.0.2",
    "feed": "^4.2.2",
    "tiny-invariant": "^1.3.1"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20230518.0",
    "@remix-run/dev": "^2.0.0",
    "@remix-run/eslint-config": "^2.0.0",
    "@types/react": "^18.2.20",
    "@types/react-dom": "^18.2.7",
    "eslint": "^8.38.0",
    "tailwindcss": "^3.3.3",
    "@tailwindcss/typography": "^0.5.9",
    "typescript": "^5.1.6"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
""",
    "blog/app/root.tsx": """
import type { LinksFunction, LoaderFunction, MetaFunction } from "@remix-run/cloudflare";
import {
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
} from "@remix-run/react";
import { json } from "@remix-run/cloudflare";
import { useTranslation } from "react-i18next";
import { useChangeLanguage } from "remix-i18next";
import i18next from "~/utils/i18n.server";
import styles from "./styles/tailwind.css";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: styles },
];

export const loader: LoaderFunction = async ({ request }) => {
  const locale = await i18next.getLocale(request);
  return json({ locale });
};

export const meta: MetaFunction = () => ({
  charset: "utf-8",
  viewport: "width=device-width,initial-scale=1",
});

export default function App() {
  const { locale } = useLoaderData<{ locale: string }>();
  const { i18n } = useTranslation();

  useChangeLanguage(locale);

  return (
    <html lang={locale} dir={i18n.dir()}>
      <head>
        <Meta />
        <Links />
      </head>
      <body className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <Outlet />
        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}
""",
    "blog/app/components/Layout.tsx": """
import { Link } from "@remix-run/react";
import { useTranslation } from "react-i18next";
import ThemeToggle from "./ThemeToggle";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { t } = useTranslation();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <header className="mb-8">
        <nav className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold">
            {t("siteName")}
          </Link>
          <ul className="flex space-x-4 items-center">
            <li>
              <Link to="/" className="hover:underline">
                {t("home")}
              </Link>
            </li>
            <li>
              <Link to="/about" className="hover:underline">
                {t("about")}
              </Link>
            </li>
            <li>
              <ThemeToggle />
            </li>
          </ul>
        </nav>
      </header>
      <main>{children}</main>
      <footer className="mt-8 text-center text-gray-500">
        © {new Date().getFullYear()} {t("siteName")}. {t("allRightsReserved")}
      </footer>
    </div>
  );
}
""",
    "blog/app/components/BlogPost.tsx": """
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
""",
    "blog/app/components/CommentSystem.tsx": """
import { useState } from "react";
import { useTranslation } from "react-i18next";

interface Comment {
  id: number;
  author: string;
  content: string;
  date: string;
}

export default function CommentSystem({ postSlug }: { postSlug: string }) {
  const { t } = useTranslation();
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newComment.trim()) {
      const comment: Comment = {
        id: Date.now(),
        author: "Anonymous",
        content: newComment,
        date: new Date().toLocaleString(),
      };
      setComments([...comments, comment]);
      setNewComment("");
    }
  };

  return (
    <div className="mt-8">
      <h3 className="text-xl font-bold mb-4">{t("comments")}</h3>
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder={t("leaveComment")}
          rows={3}
        />
        <button
          type="submit"
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {t("submitComment")}
        </button>
      </form>
      <div className="space-y-4">
        {comments.map((comment) => (
          <div key={comment.id} className="border-b pb-2">
            <p className="font-bold">{comment.author}</p>
            <p>{comment.content}</p>
            <p className="text-sm text-gray-500">{comment.date}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
""",
    "blog/app/components/Pagination.tsx": """
import { Link } from "@remix-run/react";
import { useTranslation } from "react-i18next";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
}

export default function Pagination({ currentPage, totalPages }: PaginationProps) {
  const { t } = useTranslation();

  return (
    <div className="flex justify-center space-x-2 mt-8">
      {currentPage > 1 && (
        <Link
          to={`/page/${currentPage - 1}`}
          className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded"
        >
          {t("previous")}
        </Link>
      )}
      {currentPage < totalPages && (
        <Link
          to={`/page/${currentPage + 1}`}
          className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded"
        >
          {t("next")}
        </Link>
      )}
    </div>
  );
}
""",
    "blog/app/components/Search.tsx": """
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
""",
    "blog/app/components/SEO.tsx": """
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
""",
    "blog/app/components/SocialShare.tsx": """
import { useTranslation } from "react-i18next";

interface SocialShareProps {
  title: string;
  url: string;
}

export default function SocialShare({ title, url }: SocialShareProps) {
  const { t } = useTranslation();
  const fullUrl = `https://yourblog.com${url}`;

  return (
    <div className="flex space-x-2">
      <a
        href={`https://www.weibo.com/share/share.php?url=${encodeURIComponent(fullUrl)}&title=${encodeURIComponent(title)}`}
        target="_blank"
        rel="noopener noreferrer"
        className="px-2 py-1 bg-red-500 text-white rounded"
      >
        {t("shareWeibo")}
      </a>
      <a
        href={`https://twitter.com/intent/tweet?url=${encodeURIComponent(fullUrl)}&text=${encodeURIComponent(title)}`}
        target="_blank"
        rel="noopener noreferrer"
        className="px-2 py-1 bg-blue-400 text-white rounded"
      >
        {t("shareTwitter")}
      </a>
    </div>
  );
}
""",
    "blog/app/components/ThemeToggle.tsx": """
import { useTheme } from "~/hooks/useTheme";

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700"
    >
      {theme === "dark" ? "🌞" : "🌙"}
    </button>
  );
}
""",
    "blog/app/hooks/useTheme.ts": """
import { useState, useEffect } from "react";

export function useTheme() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      setTheme(savedTheme);
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      setTheme("dark");
    }
  }, []);

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  return { theme, setTheme };
}
""",
    "blog/app/locales/zh.json": json.dumps({
  "siteName": "我的博客",
  "home": "首页",
  "about": "关于",
  "allRightsReserved": "版权所有",
  "comments": "评论",
  "leaveComment": "留下评论",
  "submitComment": "提交评论",
  "previous": "上一页",
  "next": "下一页",
  "searchPosts": "搜索文章...",
  "shareWeibo": "分享到微博",
  "shareTwitter": "分享到Twitter",
  "latestPosts": "最新文章"
}, indent=2),
    "blog/app/locales/en.json": json.dumps({
  "siteName": "My Blog",
  "home": "Home",
  "about": "About",
  "allRightsReserved": "All rights reserved",
  "comments": "Comments",
  "leaveComment": "Leave a comment",
  "submitComment": "Submit comment",
  "previous": "Previous",
  "next": "Next",
  "searchPosts": "Search posts...",
  "shareWeibo": "Share on Weibo",
  "shareTwitter": "Share on Twitter",
  "latestPosts": "Latest Posts"
}, indent=2),
    "blog/app/posts/example-post.md": """
---
title: 示例博客文章
date: 2023-05-20
description: 这是一篇示例博客文章
categories:
  - 技术
  - Web开发
---

# 示例博客文章

这是您博客文章的内容。您可以在这里使用Markdown语法。

## 子标题

- 列表项1
- 列表项2
- 列表项3

[链接到另一个页面](https://example.com)
""",
    "blog/app/routes/index.tsx": """
import { json } from "@remix-run/cloudflare";
import { useLoaderData } from "@remix-run/react";
import { useTranslation } from "react-i18next";
import Layout from "~/components/Layout";
import BlogPost from "~/components/BlogPost";
import Search from "~/components/Search";
import Pagination from "~/components/Pagination";
import { getSortedPostsData } from "~/utils/markdown";
import { paginate } from "~/utils/pagination";
import { SEO } from "~/components/SEO";

export const meta = SEO({
  title: "我的现代博客",
  description: "欢迎来到我的使用Remix构建的现代博客",
  url: "https://yourblog.com",
});

export const loader = async () => {
  const allPosts = getSortedPostsData();
  const { items: posts, ...pagination } = paginate(allPosts, 1, 10);
  return json({ posts, pagination });
};

export default function Index() {
  const { posts, pagination } = useLoaderData<typeof loader>();
  const { t } = useTranslation();

  return (
    <Layout>
      <h1 className="text-3xl font-bold mb-8">{t("latestPosts")}</h1>
      <Search posts={posts} />
      <div className="space-y-8">
        {posts.map((post) => (
          <BlogPost key={post.slug} {...post} />
        ))}
      </div>
      <Pagination currentPage={1} totalPages={pagination.totalPages} />
    </Layout>
  );
}
""",
    "blog/app/routes/posts/$slug.tsx": """
import { json } from "@remix-run/cloudflare";
import { useLoaderData } from "@remix-run/react";
import invariant from "tiny-invariant";
import { useTranslation } from "react-i18next";
import Layout from "~/components/Layout";
import CommentSystem from "~/components/CommentSystem";
import { getPostData } from "~/utils/markdown";
import { SEO } from "~/components/SEO";

export const loader = async ({ params }: { params: { slug: string } }) => {
  invariant(params.slug, "Expected params.slug");
  const post = await getPostData(params.slug);
  return json({ post });
};

export const meta = ({ data }: { data: { post: ReturnType<typeof getPostData> } }) => {
  return SEO({
    title: data.post.title,
    description: data.post.description,
    url: `https://yourblog.com/posts/${data.post.slug}`,
  });
};

export default function Post() {
  const { post } = useLoaderData<typeof loader>();
  const { t } = useTranslation();

  return (
    <Layout>
      <article className="prose dark:prose-invert max-w-none">
        <h1>{post.title}</h1>
        <p className="text-gray-500">{post.date}</p>
        <div dangerouslySetInnerHTML={{ __html: post.contentHtml }} />
      </article>
      <CommentSystem postSlug={post.slug} />
    </Layout>
  );
}
""",
    "blog/app/utils/i18n.server.ts": """
import { RemixI18Next } from "remix-i18next";
import { createCookie } from "@remix-run/cloudflare";
import Backend from "i18next-fs-backend";
import { resolve } from "node:path";

const i18next = new RemixI18Next({
  detection: {
    supportedLanguages: ["en", "zh"],
    fallbackLanguage: "zh",
  },
  i18next: {
    backend: {
      loadPath: resolve("./public/locales/{{lng}}/{{ns}}.json"),
    },
  },
  backend: Backend,
});

export default i18next;
""",
    "blog/app/utils/markdown.ts": """
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { remark } from "remark";
import html from "remark-html";

const postsDirectory = path.join(process.cwd(), "app/posts");

export async function getPostData(slug: string) {
  const fullPath = path.join(postsDirectory, `${slug}.md`);
  const fileContents = fs.readFileSync(fullPath, "utf8");

  const { data, content } = matter(fileContents);

  const processedContent = await remark().use(html).process(content);
  const contentHtml = processedContent.toString();

  return {
    slug,
    contentHtml,
    ...(data as { title: string; date: string; description: string; categories: string[] }),
  };
}

export function getAllPostSlugs() {
  const fileNames = fs.readdirSync(postsDirectory);
  return fileNames.map((fileName) => fileName.replace(/\.md$/, ""));
}

export function getSortedPostsData() {
  const fileNames = fs.readdirSync(postsDirectory);
  const allPostsData = fileNames.map((fileName) => {
    const slug = fileName.replace(/\.md$/, "");
    const fullPath = path.join(postsDirectory, fileName);
    const fileContents = fs.readFileSync(fullPath, "utf8");
    const { data } = matter(fileContents);

    return {
      slug,
      ...(data as { title: string; date: string; description: string; categories: string[] }),
    };
  });

  return allPostsData.sort((a, b) => (a.date < b.date ? 1 : -1));
}
""",
    "blog/app/utils/pagination.ts": """
export function paginate<T>(items: T[], page: number, perPage: number) {
  const offset = (page - 1) * perPage;
  const totalPages = Math.ceil(items.length / perPage);

  const paginatedItems = items.slice(offset, offset + perPage);

  return {
    previousPage: page - 1 ? page - 1 : null,
    nextPage: totalPages > page ? page + 1 : null,
    total: items.length,
    totalPages: totalPages,
    items: paginatedItems,
  };
}
""",
    "blog/app/utils/rss.ts": """
import { Feed } from "feed";
import { getSortedPostsData } from "./markdown";

export function generateRssFeed() {
  const posts = getSortedPostsData();
  const siteURL = "https://yourblog.com";
  const date = new Date();

  const feed = new Feed({
    title: "您的博客名称",
    description: "您的博客描述",
    id: siteURL,
    link: siteURL,
    language: "zh",
    image: `${siteURL}/favicon.png`,
    favicon: `${siteURL}/favicon.ico`,
    copyright: `版权所有 ${date.getFullYear()}, 您的名字`,
    updated: date,
    feedLinks: {
      rss2: `${siteURL}/rss/feed.xml`,
      json: `${siteURL}/rss/feed.json`,
      atom: `${siteURL}/rss/atom.xml`,
    },
    author: {
      name: "您的名字",
      email: "your-email@example.com",
      link: siteURL,
    },
  });

  posts.forEach((post) => {
    feed.addItem({
      title: post.title,
      id: `${siteURL}/posts/${post.slug}`,
      link: `${siteURL}/posts/${post.slug}`,
      description: post.description,
      content: post.description,
      author: [
        {
          name: "您的名字",
          email: "your-email@example.com",
          link: siteURL,
        },
      ],
      date: new Date(post.date),
    });
  });

  return feed;
}
""",
    "blog/remix.config.js": """
/** @type {import('@remix-run/dev').AppConfig} */
module.exports = {
  serverBuildTarget: "cloudflare-pages",
  server: "./server.js",
  ignoredRouteFiles: ["**/.*"],
  future: {
    v2_errorBoundary: true,
    v2_meta: true,
    v2_normalizeFormMethod: true,
    v2_routeConvention: true,
  },
  serverModuleFormat: "cjs",
};
""",
    "blog/tailwind.config.js": """
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
  ],
};
""",
    "blog/public/_routes.json": """
{
  "version": 1,
  "include": ["/*"],
  "exclude": ["/build/*"]
}
"""
}

# Create files
for file_path, content in files.items():
    create_file(file_path, content)