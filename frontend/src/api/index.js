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

export async function getCharacters() {
    try {
        const response = await api.get("/characters");
        return {
            success: true,
            data: response.data.data,
        };
    } catch (error) {
        console.error("Get characters error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || "Failed to load characters",
        };
    }
}

export async function getPlayerCharacters(playerName) {
    try {
        const response = await api.get(`/player/${playerName}/characters`);
        return {
            success: true,
            data: response.data.data,
        };
    } catch (error) {
        console.error("Get player characters error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to load ${playerName}'s characters`,
        };
    }
}

export async function addPlayerCharacters(playerName, characters) {
    try {
        const response = await api.post(`/player/${playerName}/characters`, {
            characters: characters,
        });
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        console.error("Add player characters error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to add characters to ${playerName}`,
        };
    }
}

export async function deletePlayerCharacters(playerName, characters) {
    try {
        const response = await api.delete(`/player/${playerName}/characters`, {
            data: { characters: characters },
        });
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        console.error("Delete player characters error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to delete characters to ${playerName}`,
        };
    }
}

export async function getWeapons() {
    try {
        const response = await api.get("/weapons");
        return {
            success: true,
            data: response.data.data,
        };
    } catch (error) {
        console.error("Get weapons error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || "Failed to load weapons",
        };
    }
}

export async function getPlayerWeapons(playerName) {
    try {
        const response = await api.get(`/player/${playerName}/weapons`);
        return {
            success: true,
            data: response.data.data,
        };
    } catch (error) {
        console.error("Get player weapons error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to load ${playerName}'s weapons`,
        };
    }
}

export async function addPlayerWeapons(playerName, weapons) {
    try {
        const response = await api.post(`/player/${playerName}/weapons`, {
            weapons: weapons,
        });
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        console.error("Add player weapons error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to add weapons to ${playerName}`,
        };
    }
}

export async function deletePlayerWeapons(playerName, weapons) {
    try {
        const response = await api.delete(`/player/${playerName}/weapons`, {
            data: { weapons: weapons },
        });
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        console.error("Delete player weapons error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to delete weapons to ${playerName}`,
        };
    }
}

export async function getPlayerScreenshots(playerName) {
    try {
        const response = await api.get(`/player/${playerName}/screenshots`);
        return {
            success: true,
            data: response.data.data,
        };
    } catch (error) {
        console.error("Get player screenshots error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to load ${playerName}'s screenshots`,
        };
    }
}

export async function uploadPlayerScreenshot(playerName, file) {
    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await api.post(`/player/${playerName}/screenshots`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        console.error("Upload screenshot error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to upload screenshot for ${playerName}`,
        };
    }
}

export async function updateDisplayName(displayName) {
    try {
        const response = await api.post(`/player/name`, {
            newDisplayName: displayName,
        });
        return {
            success: true,
            data: response.data,
        };
    } catch (error) {
        console.error("Change player display name error:", error.response?.data || error.message);
        return {
            success: false,
            error: error.response?.data?.message || `Failed to change player display name`,
        };
    }
}
