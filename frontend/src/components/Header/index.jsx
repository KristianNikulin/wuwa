import React from "react";
import { useNavigate } from "react-router-dom";

import { PROJECT_NAME } from "../../constants/text";

import styles from "./styles.module.scss";

const Header = () => {
    const navigate = useNavigate();

    // запрос на проверку логина -> доступ в профиль

    const isLogged = false;

    const nickname = "kr1sn1k";

    return (
        <header className={styles.appHeader}>
            <div className={styles.wrapper}>
                <h1 className={styles.name}>{PROJECT_NAME}</h1>
                <div className={styles.links}>
                    <button onClick={() => navigate("/about")}>ABOUT</button>
                    <button onClick={() => navigate("/rules")}>RULES</button>
                    <button onClick={() => navigate("/bracket")}>TOURNAMENT BRACKET</button>
                    {!isLogged && <button onClick={() => navigate("/participate")}>PARTICIPATE</button>}
                    {!isLogged && <button onClick={() => navigate(`/player/${nickname}`)}>{nickname}</button>}
                </div>
                <div className={styles.infoContainer}>
                    @zymer44
                    <img src="../../images/tg.png" alt="" />
                </div>
            </div>
        </header>
    );
};

export default Header;
