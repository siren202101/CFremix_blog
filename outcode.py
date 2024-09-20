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
    "package.json",
    "app/root.tsx",
    "app/components/Layout.tsx",
    "app/components/BlogPost.tsx",
    "app/components/CommentSystem.tsx",
    "app/components/Pagination.tsx",
    "app/components/Search.tsx",
    "app/components/SEO.tsx",
    "app/components/SocialShare.tsx",
    "app/components/ThemeToggle.tsx",
    "app/hooks/useTheme.ts",
    "app/locales/zh.json",
    "app/locales/en.json",
    "app/posts/example-post.md",
    "app/routes/index.tsx",
    "app/routes/posts/$slug.tsx",
    "app/utils/i18n.server.ts",
    "app/utils/markdown.ts",
    "app/utils/pagination.ts",
    "app/utils/rss.ts",
    "remix.config.js",
    "tailwind.config.js",
    "public/_routes.json",
    "functions/[[path]].js",
    "server.js",

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