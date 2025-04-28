import React from "react";

import Header from "../../components/Header";
import Button from "../../components/Button";
import TwitchStreamers from "../../components/TwitchStreamers";
import Input from "../../components/Input";

import styles from "./styles.module.scss";

const Player = () => {
    return (
        <div className={styles.rulesContainer}>
            <Header />
            <div className={styles.participateContent}>ABOBA</div>
            <div>
                <TwitchStreamers />
            </div>
        </div>
    );
};

export default Player;
