import React from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import Header from "../../components/Header";
import Button from "../../components/Button";
import TwitchStreamers from "../../components/TwitchStreamers";
import Input from "../../components/Input";

import styles from "./styles.module.scss";

const Player = () => {
    const navigate = useNavigate();

    const methods = useForm();

    const onSubmit = (data) => {
        console.log(data);

        navigate(`/player/${data.login}`);
        // запрос на авторизацию -> переход на страницу игрока
    };

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
