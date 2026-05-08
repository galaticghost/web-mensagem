import i18n from "i18next"
import LanguageDetector from "i18next-browser-languagedetector"
import { initReactI18next } from "react-i18next";

import ptBR from "./locales/pt-br.json";
import enUS from "./locales/en-us.json";

i18n.use(LanguageDetector).use(initReactI18next).init({
    resources: {
        "pt-BR": {
            translation: ptBR
        },
        "en-US": {
            translation: enUS
        }
    },
    fallbackLng: "en-US",
    debug: false,
    interpolation: {
        escapeValue: false
    }
})