
import { RemixI18Next } from "remix-i18next";
import { createCookie } from "@remix-run/cloudflare";
import Backend from "i18next-fs-backend";
import { resolve } from "node:path";

const i18next = new RemixI18Next({
  detection: {
    supportedLanguages: ["en", "zh"],
    fallbackLanguage: "zh",
  },
  i18next: {
    backend: {
      loadPath: resolve("./public/locales/{{lng}}/{{ns}}.json"),
    },
  },
  backend: Backend,
});

export default i18next;
