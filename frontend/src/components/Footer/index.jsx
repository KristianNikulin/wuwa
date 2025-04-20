import React from "react";

import styles from "./styles.module.scss";

// призовые места
const items = [{ name: "призовой фонд", price: 150 }];

const Footer = () => {
    return (
        <footer className={styles.footerContainer}>
            <div className={styles.items}>
                {items.map((item, i) => (
                    <p key={i}>
                        {item.name} - {item.price}$
                    </p>
                ))}
            </div>
        </footer>
    );
};

export default Footer;
