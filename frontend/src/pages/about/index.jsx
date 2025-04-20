import React from "react";

import Header from "../../components/Header";
import Footer from "../../components/Footer";

import styles from "./styles.module.scss";

const About = () => {
    return (
        <div className={styles.aboutContainer}>
            <Header />
            <div className={styles.mainContent}>
                <div className={styles.title}>
                    tempest <img style={{ width: "100px", height: "100px" }} src="../../images/demon.png" alt="" /> cup
                </div>
                <div className={styles.subtitle}>
                    <span className={styles.firstName}>miroichii</span>
                    <img style={{ width: "50px", height: "50px" }} src="../../images/twich.png" alt="" />
                    <span className={styles.secondName}>maliwan</span>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default About;
