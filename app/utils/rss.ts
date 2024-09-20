
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
