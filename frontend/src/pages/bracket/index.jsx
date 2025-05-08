import React from "react";
import { Bracket } from "react-brackets";

import Header from "../../components/Header";
import TwitchStreamers from "../../components/TwitchStreamers";

import styles from "./styles.module.scss";

const Brackets = () => {
    const firstRoundSeeds = Array.from({ length: 16 }, (_, i) => ({
        id: i + 1,
        teams: [
            { name: `Team ${String.fromCharCode(65 + i * 2)}` }, // A, C, E, ...
            { name: `Team ${String.fromCharCode(66 + i * 2)}` }, // B, D, F, ...
        ],
    }));

    const rounds = [
        {
            title: "Round of 32",
            seeds: firstRoundSeeds,
        },
        {
            title: "Round of 16",
            seeds: Array.from({ length: 8 }, (_, i) => ({
                id: 17 + i,
                teams: [{ name: `Winner ${i * 2 + 1}` }, { name: `Winner ${i * 2 + 2}` }],
            })),
        },
        {
            title: "Quarterfinals",
            seeds: Array.from({ length: 4 }, (_, i) => ({
                id: 25 + i,
                teams: [{ name: `Winner ${17 + i * 2}` }, { name: `Winner ${18 + i * 2}` }],
            })),
        },
        {
            title: "Semifinals",
            seeds: Array.from({ length: 2 }, (_, i) => ({
                id: 29 + i,
                teams: [{ name: `Winner ${25 + i * 2}` }, { name: `Winner ${26 + i * 2}` }],
            })),
        },
        {
            title: "Final",
            seeds: [
                {
                    id: 31,
                    teams: [{ name: "Winner 29" }, { name: "Winner 30" }],
                },
            ],
        },
    ];

    return (
        <div className={styles.bracketContainer}>
            <Header />
            <div className={styles.bracketContent}>
                <Bracket rounds={rounds} />
            </div>
            {/* <div style={{ zIndex: 1 }}>
                <TwitchStreamers />
            </div> */}
        </div>
    );
};

export default Brackets;
