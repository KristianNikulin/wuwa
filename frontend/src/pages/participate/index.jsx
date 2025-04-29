import React, { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useUser } from "../../state-providers/UserContext";
import { api } from "../../api";

import Header from "../../components/Header";
import Button from "../../components/Button";
import TwitchStreamers from "../../components/TwitchStreamers";
import Input from "../../components/Input";

import styles from "./styles.module.scss";

const Participate = () => {
    const [isLoginError, setIsLoginError] = useState(false);
    const navigate = useNavigate();

    const { checkAuth } = useUser();

    const methods = useForm();

    const onSubmit = async (data) => {
        try {
            const response = await api.post("/login", {
                username: data.login,
                password: data.password,
            });

            const name = response?.data?.user?.username || "";

            navigate(`/player/${name}`);
            setIsLoginError(false);
            checkAuth();
        } catch (error) {
            if (error?.response?.status == 401) {
                setIsLoginError(true);
            }
        }
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
                        {isLoginError && <div className={styles.errorLoginBlock}>Неверный ник или пароль</div>}
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
