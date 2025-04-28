import axios from "axios";

import { BACKEND_URL } from "../constants";

export const api = axios.create({
    baseURL: BACKEND_URL,
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    },
});

export async function checkSession() {
    try {
        const response = await api.get("/check_session");
        const data = response.data;

        if (data.is_logged_in) {
            console.log("User is logged in:", data.user);
            return data.user;
        } else {
            console.log("User is not logged in");
            return null;
        }
    } catch (error) {
        console.error("Session check failed:", error);
        return null;
    }
}
