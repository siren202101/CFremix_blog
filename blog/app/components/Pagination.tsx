
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
