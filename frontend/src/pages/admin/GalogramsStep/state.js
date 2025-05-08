import { useEffect, useState } from "react";
import { getPlayers, getActiveTournament } from "../../../api";
import { useAdmin } from "../../../state-providers/AdminContext";

export const useGalogramsState = () => {
    const { updateState } = useAdmin();

    const [players, setPlayers] = useState([]);
    const [activeTournament, setActiveTournament] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            setIsLoading(true);
            setError(null);

            try {
                // Загружаем данные параллельно
                const [playersResult, tournamentResult] = await Promise.all([getPlayers(), getActiveTournament()]);

                console.log("Players loaded:", playersResult);
                console.log("Active tournament:", tournamentResult);

                // Обрабатываем результаты
                const errors = [];

                if (playersResult.success) {
                    setPlayers(playersResult.data || []);
                } else {
                    errors.push(playersResult.error);
                }

                if (tournamentResult.success) {
                    updateState("tournament", tournamentResult.data);
                    setActiveTournament(tournamentResult.data);
                } else {
                    errors.push(tournamentResult.error);
                }

                // Если есть ошибки, объединяем их
                if (errors.length > 0) {
                    setError(errors.join("; "));
                }
            } catch (err) {
                console.error("Error loading data:", err);
                setError(err.message || "Failed to load data");
            } finally {
                setIsLoading(false);
            }
        };

        loadData();
    }, []);

    return {
        players,
        activeTournament,
        isLoading,
        error,
    };
};
