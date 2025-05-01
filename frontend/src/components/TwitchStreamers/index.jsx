import React from "react";

import twitchImg from "../../images/twitch.png";

import styles from "./styles.module.scss";

const TwitchStreamers = () => {
    return (
        <div className={styles.container}>
            <img style={{ width: "50px", height: "50px" }} src={twitchImg} alt="" />
            <div className={styles.streamers}>
                <span className={styles.firstName}>miroichii</span>
                <br />
                <span className={styles.secondName}>maliwan</span>
            </div>
        </div>
    );
};

export default TwitchStreamers;
