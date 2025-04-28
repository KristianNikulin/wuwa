import React from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../../state-providers/UserContext";

import styles from "./styles.module.scss";

const Header = () => {
    const navigate = useNavigate();

    const { user, isLoading, updateUser, checkAuth } = useUser();

    return (
        <header className={styles.appHeader}>
            <div className={styles.wrapper}>
                <h1 className={styles.name}>
                    Wuthering <br /> Waves
                </h1>
                <div className={styles.links}>
                    <button onClick={() => navigate("/about")}>ABOUT</button>
                    <button onClick={() => navigate("/rules")}>RULES</button>
                    <button onClick={() => navigate("/bracket")}>TOURNAMENT BRACKET</button>
                    {!isLoading && !user && <button onClick={() => navigate("/participate")}>PARTICIPATE</button>}
                    {!isLoading && user && (
                        <button onClick={() => navigate(`/player/${user.username}`)}>{user.display_name}</button>
                    )}
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
