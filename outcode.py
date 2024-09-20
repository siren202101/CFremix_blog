import os

def print_file_content(file_path):
    """Prints the content of a file with a formatted header.

    Args:
        file_path (str): The path to the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"文件名：{file_path}\n文件内容：\n{content}\n\n")

def main():
    """Main function to read and print file contents."""
    file_list = [
    "blog/package.json",
    "blog/app/root.tsx",
    "blog/app/components/Layout.tsx",
    "blog/app/components/BlogPost.tsx",
    "blog/app/components/CommentSystem.tsx",
    "blog/app/components/Pagination.tsx",
    "blog/app/components/Search.tsx",
    "blog/app/components/SEO.tsx",
    "blog/app/components/SocialShare.tsx",
    "blog/app/components/ThemeToggle.tsx",
    "blog/app/hooks/useTheme.ts",
    "blog/app/locales/zh.json",
    "blog/app/locales/en.json",
    "blog/app/posts/example-post.md",
    "blog/app/routes/index.tsx",
    "blog/app/routes/posts/$slug.tsx",
    "blog/app/utils/i18n.server.ts",
    "blog/app/utils/markdown.ts",
    "blog/app/utils/pagination.ts",
    "blog/app/utils/rss.ts",
    "blog/remix.config.js",
    "blog/tailwind.config.js",
    "blog/public/_routes.json",
    "blog/functions/[[path]].js",
    "blog/server.js",

]

    with open("output.txt", "w", encoding="utf-8") as output_file:
        for file_path in file_list:
            try:
                print_file_content(file_path)
                # 将输出同时写入到文件
                output_file.write(f"文件名：{file_path}\n")
                with open(file_path, "r", encoding="utf-8") as f:
                    output_file.write(f"文件内容：\n{f.read()}\n\n")
            except FileNotFoundError:
                print(f"文件未找到: {file_path}")

if __name__ == "__main__":
    main()