import { useEffect, useMemo, useState } from "react";
import { getPlayerCharacters } from "../../../api";

export const usePickBansState = (player1, player2) => {
    const [player1Characters, setPlayer1Characters] = useState([]);
    const [player2Characters, setPlayer2Characters] = useState([]);

    const uniqueCharacters = useMemo(() => {
        const combined = [...player1Characters, ...player2Characters];
        return combined.filter((character, index, self) => self.findIndex((c) => c.name === character.name) === index);
    }, [player1Characters, player2Characters]);

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadCharacters = async () => {
            if (!player1 || !player2) return;

            setIsLoading(true);
            setError(null);

            try {
                const [result1, result2] = await Promise.all([
                    getPlayerCharacters(player1),
                    getPlayerCharacters(player2),
                ]);

                console.log("Player 1 characters:", result1);
                console.log("Player 2 characters:", result2);

                if (result1.success && result2.success) {
                    setPlayer1Characters(result1.data || []);
                    setPlayer2Characters(result2.data || []);
                } else {
                    const errorMessage =
                        (!result1.success ? result1.error + " " : "") + (!result2.success ? result2.error : "");
                    setError(errorMessage.trim() || "Failed to load players' characters");
                }
            } catch (err) {
                console.error("Error loading characters:", err);
                setError(err.message || "Failed to load players' characters");
            } finally {
                setIsLoading(false);
            }
        };

        loadCharacters();
    }, [player1, player2]);

    return {
        player1Characters,
        player2Characters,
        uniqueCharacters,
        isLoading,
        error,
    };
};
