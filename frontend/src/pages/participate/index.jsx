import React from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import Header from "../../components/Header";
import Button from "../../components/Button";
import TwitchStreamers from "../../components/TwitchStreamers";
import Input from "../../components/Input";

import styles from "./styles.module.scss";

const Participate = () => {
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
            <div className={styles.participateContent}>
                <div className={styles.participateTitleContent}>
                    <div className={styles.participateTitle}>прием заявок на участие</div>
                    <div>
                        <Button>
                            <p style={{ fontSize: "27px" }}>участвовать</p>
                        </Button>
                    </div>
                </div>
                <div>
                    {/* можно вынести в отдельный компонент */}
                    <FormProvider {...methods}>
                        <form className={styles.participateLoginForm} onSubmit={methods.handleSubmit(onSubmit)}>
                            <Input id="login" placeholder="username" />
                            <Input id="password" type="password" placeholder="password" />
                            <Button type="submit">
                                <p style={{ fontSize: "21px" }}>send</p>
                            </Button>
                        </form>
                    </FormProvider>
                </div>
            </div>
            <div>
                <TwitchStreamers />
            </div>
        </div>
    );
};

export default Participate;
