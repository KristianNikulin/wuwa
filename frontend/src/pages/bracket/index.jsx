import React from "react";
import { Bracket } from "react-brackets";

import Header from "../../components/Header";
import TwitchStreamers from "../../components/TwitchStreamers";

import styles from "./styles.module.scss";

const Brackets = () => {
    const rounds = [
        {
            title: "Round one",
            seeds: [
                {
                    id: 1,
                    // date: new Date().toDateString(),
                    teams: [{ name: "q" }, { name: "w" }],
                },
                {
                    id: 2,
                    teams: [{ name: "e" }, { name: "r" }],
                },
                {
                    id: 3,
                    teams: [{ name: "t" }, { name: "y" }],
                },
                {
                    id: 4,
                    teams: [{ name: "u" }, { name: "i" }],
                },
            ],
        },
        {
            title: "Round two",
            seeds: [
                {
                    id: 5,
                    teams: [{ name: "q" }, { name: "e" }],
                },
                {
                    id: 6,
                    teams: [{ name: "t" }, { name: "u" }],
                },
            ],
        },
        {
            title: "Round three",
            seeds: [
                {
                    id: 5,
                    teams: [{ name: "q" }, { name: "t" }],
                },
            ],
        },
    ];

    return (
        <div className={styles.bracketContainer}>
            <Header />
            <div className={styles.bracketContent}>
                <Bracket rounds={rounds} />
                <Bracket rounds={rounds} />
            </div>
            <div style={{ zIndex: 1 }}>
                <TwitchStreamers />
            </div>
        </div>
    );
};

export default Brackets;
