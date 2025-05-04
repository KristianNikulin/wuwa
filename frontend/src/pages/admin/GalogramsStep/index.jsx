import React, { useState } from "react";
import { useAdminForm } from "../../../state-providers/AdminContext";

import { galogramsData } from "../../../constants/videoImports";

import styles from "./styles.module.scss";

export const GalogramsStep = () => {
    const { nextStep } = useAdminForm();

    const [bannedGalograms, setBannedGalograms] = useState([]);
    const [choosedGalograms, setChoosedGalograms] = useState([]);
    const [clickCount, setClickCount] = useState(0);

    const handleVideoClick = (videoId) => {
        const isChoosed = choosedGalograms.includes(videoId) || bannedGalograms.includes(videoId);
        const newClickCount = clickCount + 1;
        if (!isChoosed && newClickCount <= 4) {
            setClickCount(newClickCount);
            if (newClickCount <= 2) {
                setBannedGalograms((prev) => [...prev, videoId]);
            } else {
                setChoosedGalograms((prev) => [...prev, videoId]);
            }
        }
    };

    const handleRandomSelect = () => {
        const available = galogramsData.filter(
            (g) => !(choosedGalograms.includes(g.id) || bannedGalograms.includes(g.id))
        );
        const randomIndex = Math.floor(Math.random() * available.length);
        const randomId = available[randomIndex]?.id;

        if (clickCount == 4) {
            setClickCount((click) => click + 1);
            setChoosedGalograms((prev) => [...prev, randomId]);
        }
    };

    const handleReset = () => {
        setChoosedGalograms([]);
        setBannedGalograms([]);
        setClickCount(0);
    };

    return (
        <div className={styles.galogramsContent}>
            <div className={styles.videoContent}>
                {galogramsData.map(({ id, video, element }) => {
                    const isChoosedSelected = choosedGalograms.includes(id);
                    const isBannedSelected = bannedGalograms.includes(id);

                    return (
                        <div
                            key={id}
                            className={`${styles.videoContainer} ${isChoosedSelected ? styles.choosedSelected : ""} ${
                                isBannedSelected ? styles.bannedSelected : ""
                            }`}
                            onClick={() => handleVideoClick(id)}
                        >
                            <video src={video} autoPlay={!isBannedSelected} loop muted />
                            <img className={styles.element} src={element} alt="" />
                        </div>
                    );
                })}
            </div>

            <div>
                <button type="button" className={styles.actionButton} onClick={handleRandomSelect}>
                    Random Select
                </button>
                <button type="button" className={styles.actionButton} onClick={handleReset}>
                    Reset
                </button>
                <button type="button" className={styles.nextButton} onClick={nextStep}>
                    Next
                </button>
            </div>
        </div>
    );
};
