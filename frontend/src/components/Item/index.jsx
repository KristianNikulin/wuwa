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
    showTrash = true,
    showStats = true,
    canEdit = true,
    onAddClick = () => {},
    onRemoveClick = () => {},
    onValueChange = () => {},
    ...props
}) => {
    const [imageSrc, setImageSrc] = useState(null);

    const [localValue1, setLocalValue1] = useState(value1 ?? 0);
    const [localValue2, setLocalValue2] = useState(value2 ?? (type === "weapon" ? 1 : 0));

    useEffect(() => {
        setLocalValue1(value1 ?? 0);
        setLocalValue2(value2 ?? (type === "weapon" ? 1 : 0));
    }, [value1, value2, type]);

    const handleBlur = (field) => (e) => {
        let value = e.target.value;

        if (value === "") {
            if (field === "value1") {
                value = 0;
                setLocalValue1(value);
            } else if (field === "value2") {
                value = type === "weapon" ? 1 : 0;
                setLocalValue2(value);
            }
        }

        onValueChange(
            name,
            field === "value1" ? parseInt(value) || 0 : localValue1,
            field === "value2" ? parseInt(value) || (type === "weapon" ? 1 : 0) : localValue2
        );
    };

    const handleValue1Change = (e) => {
        const input = e.target.value;

        if (/^\d*$/.test(input)) {
            const max = 90;
            setLocalValue1(input === "" ? "" : Math.min(parseInt(input), max));
        }
    };

    const handleValue2Change = (e) => {
        const input = e.target.value;
        if (/^\d*$/.test(input)) {
            const max = type === "weapon" ? 5 : 6;
            setLocalValue2(input === "" ? "" : Math.min(parseInt(input), max));
        }
    };

    useEffect(() => {
        const loadImage = () => {
            try {
                let image;
                if (type === "weapon") image = weaponImages[name];
                if (type === "character") image = characterImages[name];
                setImageSrc(image);
            } catch (e) {
                console.warn(`error: `, e);
            }
        };
        type && name && loadImage();
    }, [type, name]);

    const prefix = type === "weapon" ? "R" : "C";

    return (
        <>
            {isAddButton ? (
                <div className={styles.addItemContainer}>
                    <button disabled={disabled} onClick={onAddClick} className={styles.addItem}>
                        +
                    </button>
                </div>
            ) : (
                <div onClick={onAddClick} className={styles.itemContainer} {...props}>
                    <img className={styles.itemImage} src={imageSrc} alt="" />
                    {showStats &&
                        (canEdit ? (
                            <div className={styles.valueContainer}>
                                <input
                                    className={styles.valueText}
                                    value={localValue1 === "" ? "" : localValue1}
                                    onChange={handleValue1Change}
                                    onBlur={handleBlur("value1")}
                                    type="text"
                                    inputMode="numeric"
                                    pattern="[0-9]*"
                                />{" "}
                                |{" "}
                                <span className={styles.valueText}>
                                    {prefix}
                                    <input
                                        value={localValue2 === "" ? "" : localValue2}
                                        onChange={handleValue2Change}
                                        onBlur={handleBlur("value2")}
                                        type="text"
                                        inputMode="numeric"
                                        pattern="[0-9]*"
                                    />
                                </span>
                            </div>
                        ) : (
                            <div className={styles.valueContainer}>
                                <span className={styles.valueText}>{value1}</span> |{" "}
                                <span className={styles.valueText}>
                                    {prefix}
                                    {value2}
                                </span>
                            </div>
                        ))}
                    {showTrash && (
                        <button onClick={onRemoveClick} className={styles.trashButton}>
                            <FiTrash2 className={styles.trashIcon} />
                        </button>
                    )}
                </div>
            )}
        </>
    );
};

export default Item;
