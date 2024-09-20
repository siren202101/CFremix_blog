import remixI18next from 'remix-i18next';
import { createCookie } from "@remix-run/cloudflare";
import enTranslations from "~/locales/en.json";
import zhTranslations from "~/locales/zh.json";

const i18next = new remixI18next.RemixI18Next({
  detection: {
    supportedLanguages: ["en", "zh"],
    fallbackLanguage: "zh",
  },
  i18next: {
    resources: {
      en: { translation: enTranslations },
      zh: { translation: zhTranslations },
    },
  },
});

export default i18next;