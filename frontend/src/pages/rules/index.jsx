import React from "react";

import Header from "../../components/Header";
import Button from "../../components/Button";
import TwitchStreamers from "../../components/TwitchStreamers";

import { Trans } from "@lingui/react/macro";

import styles from "./styles.module.scss";

const Rules = () => {
    return (
        <div className={styles.rulesContainer}>
            <Header />
            <div className={styles.rulesContent}>
                <div className={styles.rulesTable}>test</div>
                <div>
                    <Button style={{ minWidth: "244px" }}>
                        <Trans>RULES</Trans>
                    </Button>
                </div>
                <div className={styles.rulesTable}>test2</div>
            </div>
            <div>
                <TwitchStreamers />
            </div>
        </div>
    );
};

export default Rules;
