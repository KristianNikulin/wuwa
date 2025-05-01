import React from "react";

import Header from "../../components/Header";
import Footer from "../../components/Footer";

import styles from "./styles.module.scss";

import demonImg from "../../images/demon.png";
import twitchImg from "../../images/twitch.png";

const About = () => {
    return (
        <div className={styles.aboutContainer}>
            <Header />
            <div className={styles.mainContent}>
                <div className={styles.title}>
                    tempest{" "}
                    <img style={{ width: "150px", height: "150px", marginRight: "5px" }} src={demonImg} alt="" /> cup
                </div>
                <div className={styles.subtitle}>
                    <span className={styles.firstName}>miroichii</span>
                    <img style={{ width: "60px", height: "60px" }} src={twitchImg} alt="" />
                    <span className={styles.secondName}>maliwan</span>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default About;
