import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { i18n } from "@lingui/core";
import { I18nProvider } from "@lingui/react";
import { messages as enMessages } from "./locales/en/messages.po";
import { messages as ruMessages } from "./locales/ru/messages.po";

import App from "./pages";

import { UserProvider } from "./state-providers/UserContext";

import "./styles/index.css";

i18n.load({ en: enMessages, ru: ruMessages });
i18n.activate("en");

createRoot(document.getElementById("root")).render(
    // <StrictMode>
    <I18nProvider i18n={i18n}>
        <UserProvider>
            <App />
        </UserProvider>
    </I18nProvider>
    // </StrictMode>
);

// УБРАТЬ ВСЕ CONSOLE.LOG ПРИ ДЕПЛОЕ
