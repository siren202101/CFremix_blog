import matter from "gray-matter";
import { remark } from "remark";
import html from "remark-html";

const posts = {
  "example-post": `---
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
`,
};

export async function getPostData(slug: string) {
  const fileContents = posts[slug];
  if (!fileContents) {
    throw new Error(`Post not found: ${slug}`);
  }

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
  return Object.keys(posts);
}

export function getSortedPostsData() {
  const allPostsData = Object.entries(posts).map(([slug, content]) => {
    const { data } = matter(content);
    return {
      slug,
      ...(data as { title: string; date: string; description: string; categories: string[] }),
    };
  });

  return allPostsData.sort((a, b) => (a.date < b.date ? 1 : -1));
}