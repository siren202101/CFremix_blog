
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
