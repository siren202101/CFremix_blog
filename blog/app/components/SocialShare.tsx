
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
