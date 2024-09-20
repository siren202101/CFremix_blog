
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
