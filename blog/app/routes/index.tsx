
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
