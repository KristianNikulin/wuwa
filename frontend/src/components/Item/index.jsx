import React, { useEffect, useState } from "react";

import { characterImages, weaponImages } from "../../constants/imageImports";

import { FiTrash2 } from "react-icons/fi";

import styles from "./styles.module.scss";

const Item = ({
    type = "",
    name = "",
    value1,
    value2,
    disabled = false,
    isAddButton = false,
    onAddClick = () => {},
    onRemoveClick = () => {},
}) => {
    const [imageSrc, setImageSrc] = useState(null);

    useEffect(() => {
        const loadImage = () => {
            try {
                let image;
                if (type === "weapon") image = weaponImages[name];
                if (type === "character") image = characterImages[name];
                setImageSrc(image);
            } catch (e) {
                console.log(`e: `, e);
            }
        };
        type && name && loadImage();
    }, [type, name]);

    return (
        <>
            {isAddButton ? (
                <div className={styles.addItemContainer}>
                    <button disabled={disabled} onClick={onAddClick} className={styles.addItem}>
                        +
                    </button>
                </div>
            ) : (
                <div className={styles.itemContainer}>
                    <img className={styles.itemImage} src={imageSrc} alt="" />
                    {value1 && value2 && (
                        <div className={styles.valueContainer}>
                            <span className={styles.valueText}>{value1}</span> |{" "}
                            <span className={styles.valueText}>{value2}</span>
                        </div>
                    )}
                    <button onClick={onRemoveClick} className={styles.trashButton}>
                        <FiTrash2 className={styles.trashIcon} />
                    </button>
                </div>
            )}
        </>
    );
};

export default Item;
