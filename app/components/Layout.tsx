
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
