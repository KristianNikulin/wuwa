import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./styles/index.css";

import App from "./pages/index.jsx";

import { UserProvider } from "./state-providers/UserContext";

createRoot(document.getElementById("root")).render(
    // <StrictMode>
    <UserProvider>
        <App />
    </UserProvider>
    // </StrictMode>
);

// УБРАТЬ ВСЕ CONSOLE.LOG ПРИ ДЕПЛОЕ
