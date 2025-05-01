import React, { useEffect, useRef, useState } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { FiUpload } from "react-icons/fi";

import Header from "../../components/Header";
import Button from "../../components/Button";
import Item from "../../components/Item";
import Input from "../../components/Input";
import TwitchStreamers from "../../components/TwitchStreamers";

import { Trans } from "@lingui/react/macro";

import { useUser } from "../../state-providers/UserContext";
import { useCharactersState } from "./charactersState";
import { useWeaponsState } from "./weaponsState";
import { useScreenshotsState } from "./screenshotsState";

import styles from "./styles.module.scss";
import { updateDisplayName } from "../../api";

const Player = () => {
    const { user, checkAuth } = useUser();
    const methods = useForm({
        defaultValues: {
            nickname: user?.username || "",
        },
    });

    const {
        watch,
        formState: { isDirty },
        reset,
    } = methods;

    const fileInputRef = useRef(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isSaveDisabled, setIsSaveDisabled] = useState(true);

    const { state: charactersState, actions: charactersActions } = useCharactersState(user?.username);

    const { state: weaponsState, actions: weaponsActions } = useWeaponsState(user?.username);

    const { state: screenshotsState, actions: screenshotsActions } = useScreenshotsState(user?.username);

    useEffect(() => {
        const hasChanges = isDirty || charactersState.hasChanges || weaponsState.hasChanges;
        setIsSaveDisabled(!hasChanges);
    }, [isDirty, charactersState.hasChanges, weaponsState.hasChanges]);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            try {
                const [charsRes, weaponsRes, screenshotsRes] = await Promise.all([
                    charactersActions.loadCharacters(),
                    weaponsActions.loadWeapons(),
                    screenshotsActions.loadScreenshots(),
                ]);

                const errors = [
                    charsRes.success ? null : charsRes.error,
                    weaponsRes.success ? null : weaponsRes.error,
                    screenshotsRes.success ? null : screenshotsRes.error,
                ].filter(Boolean);

                if (errors.length > 0) {
                    setError(errors.join(", "));
                }
            } catch (err) {
                console.error("Load data error:", err);
                setError("Failed to load data");
            } finally {
                setLoading(false);
            }
        };

        user?.username && loadData();
    }, [user]);

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Проверка типа файла
        if (!["image/jpeg", "image/png"].includes(file.type)) {
            setError("Only JPG and PNG files are allowed");
            return;
        }

        // Проверка размера файла (например, до 5MB)
        if (file.size > 5 * 1024 * 1024) {
            setError("File size should be less than 5MB");
            return;
        }

        await screenshotsActions.handleUpload(file);
    };

    const triggerFileInput = () => {
        fileInputRef.current.click();
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            const newNickname = watch("nickname");
            const nicknameChanged = newNickname !== user?.username;

            if (nicknameChanged) {
                const nicknameRes = await updateDisplayName(newNickname);
                if (!nicknameRes.success) {
                    setError(nicknameRes.error);
                } else {
                    checkAuth();
                    reset();
                }
            }

            const [charsRes, weaponsRes] = await Promise.all([
                charactersActions.saveChanges(),
                weaponsActions.saveChanges(),
            ]);

            const errors = [
                charsRes.success ? null : charsRes.error,
                weaponsRes.success ? null : weaponsRes.error,
            ].filter(Boolean);

            if (errors.length > 0) {
                setError(errors.join(", "));
            }
        } catch (err) {
            console.error("Save error:", err);
            setError("Failed to save changes");
        } finally {
            setLoading(false);
        }
    };

    return (
        <FormProvider {...methods}>
            <div className={styles.playerContainer}>
                <Header />
                <div className={styles.playerContent}>
                    <div className={styles.tableContainer}>
                        <h3 className={styles.tableTitle}>
                            <Trans>CHARACTERS</Trans>
                        </h3>
                        <div className={styles.playerTable}>
                            <div className={styles.addButtonContainer}>
                                <Item isAddButton onAddClick={charactersActions.toggleDropdown} />
                                {charactersState.dropdownOpen && (
                                    <div className={styles.dropdown}>
                                        {charactersState.dropdownItems.map((item, i) => (
                                            <div
                                                key={`${item.name}${i}`}
                                                className={styles.dropdownItem}
                                                onClick={() => charactersActions.handleAddItem(item)}
                                            >
                                                {item.name}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                            {charactersState.displayItems.map((ch, i) => (
                                <Item
                                    key={`${ch.name}${i}`}
                                    type="character"
                                    name={ch.name}
                                    value1={ch.value1}
                                    value2={ch.value2}
                                    onRemoveClick={() => charactersActions.handleRemoveItem(ch.name)}
                                />
                            ))}
                        </div>
                    </div>
                    <div
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "space-between",
                            minWidth: "320px",
                            alignItems: "center",
                        }}
                    >
                        <div style={{ display: "flex", flexDirection: "column", gap: "70px" }}>
                            <div className={styles.tableContainer}>
                                <h3 className={styles.tableSubtitle}>
                                    <Trans>nickname</Trans>
                                </h3>
                                <Input
                                    value={user?.display_name || ""}
                                    id="nickname"
                                    placeholder="nickname"
                                    requiredMessage="Nickname is required"
                                />
                            </div>
                            <div className={styles.tableContainer}>
                                <h3 className={styles.tableSubtitle}>
                                    <Trans>screenshots</Trans>
                                </h3>
                                <div
                                    className={styles.playerTable}
                                    style={{ height: "200px", minWidth: "275px", overflowY: "auto" }}
                                >
                                    {screenshotsState.loading ? (
                                        <div className={styles.emptyState}>
                                            <Trans>Loading</Trans>
                                        </div>
                                    ) : screenshotsState.screenshots.length === 0 ? (
                                        <div className={styles.emptyState}>
                                            <Trans>No screenshots yet</Trans>
                                        </div>
                                    ) : (
                                        screenshotsState.screenshots.map((screenshot) => (
                                            <div key={screenshot.id} className={styles.screenshotItem}>
                                                <img
                                                    src={screenshot.url}
                                                    alt={screenshot.description || "Screenshot"}
                                                    className={styles.screenshotImage}
                                                />
                                            </div>
                                        ))
                                    )}
                                </div>

                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                    accept="image/jpeg,image/png"
                                    style={{ display: "none" }}
                                />
                                <button
                                    onClick={triggerFileInput}
                                    disabled={screenshotsState.uploading}
                                    style={{
                                        display: "flex",
                                        justifyContent: "center",
                                        marginTop: "10px",
                                    }}
                                    title="Add screenshot (jpg, png)"
                                >
                                    {screenshotsState.uploading ? "Uploading..." : <FiUpload />}
                                </button>
                                {screenshotsState.uploadError && (
                                    <div className={styles.errorText}>{screenshotsState.uploadError}</div>
                                )}
                                {screenshotsState.loadError && (
                                    <div className={styles.errorText}>{screenshotsState.loadError}</div>
                                )}
                            </div>
                        </div>
                        <Button
                            disabled={isSaveDisabled}
                            onClick={handleSave}
                            style={{ width: "205px", fontSize: "25px" }}
                        >
                            <Trans>save</Trans>
                        </Button>
                    </div>
                    <div className={styles.tableContainer}>
                        <h3 className={styles.tableTitle}>
                            <Trans>WEAPONS</Trans>
                        </h3>
                        <div className={styles.playerTable}>
                            <div className={styles.addButtonContainer}>
                                <Item isAddButton onAddClick={weaponsActions.toggleDropdown} />
                                {weaponsState.dropdownOpen && (
                                    <div className={styles.dropdown}>
                                        {weaponsState.dropdownItems.map((item, i) => (
                                            <div
                                                key={`${item.name}${i}`}
                                                className={styles.dropdownItem}
                                                onClick={() => weaponsActions.handleAddItem(item)}
                                            >
                                                {item.name}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                            {weaponsState.displayItems.map((weapon, i) => (
                                <Item
                                    key={`${weapon.name}${i}`}
                                    type="weapon"
                                    name={weapon.name}
                                    value1={weapon.value1}
                                    value2={weapon.value2}
                                    onRemoveClick={() => weaponsActions.handleRemoveItem(weapon.name)}
                                />
                            ))}
                        </div>
                    </div>
                </div>
                <div>
                    <TwitchStreamers />
                </div>
            </div>
        </FormProvider>
    );
};

export default Player;
