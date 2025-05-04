import React, { useEffect, useRef, useState } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { useParams } from "react-router-dom";

import { FiTrash2, FiUpload } from "react-icons/fi";

import Header from "../../components/Header";
import Button from "../../components/Button";
import Item from "../../components/Item";
import SkeletonItem from "../../components/SkeletonItem";
import Input from "../../components/Input";
import TwitchStreamers from "../../components/TwitchStreamers";

import { deletePlayerScreenshotById, getPlayer, updateDisplayName } from "../../api";

import { Trans } from "@lingui/react/macro";

import { useUser } from "../../state-providers/UserContext";
import { useCharactersState } from "./charactersState";
import { useWeaponsState } from "./weaponsState";
import { useScreenshotsState } from "./screenshotsState";

import styles from "./styles.module.scss";

const Player = () => {
    const { nickname } = useParams();
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

    const isAdmin = user?.status === "admin";
    const canEdit = isAdmin || nickname === user?.username;

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isSaveDisabled, setIsSaveDisabled] = useState(true);

    const { state: charactersState, actions: charactersActions } = useCharactersState(nickname);

    const { state: weaponsState, actions: weaponsActions } = useWeaponsState(nickname);

    const { state: screenshotsState, actions: screenshotsActions } = useScreenshotsState(nickname);

    const [currentUser, setCurrentUser] = useState("");

    // SCREENSHOT
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentScreenshotIndex, setCurrentScreenshotIndex] = useState(0);

    const openModal = (index) => {
        setCurrentScreenshotIndex(index);
        setIsModalOpen(true);
    };

    const closeModal = () => setIsModalOpen(false);

    const nextScreenshot = () => {
        setCurrentScreenshotIndex((prev) => (prev + 1) % screenshotsState.screenshots.length);
    };

    const prevScreenshot = () => {
        setCurrentScreenshotIndex(
            (prev) => (prev - 1 + screenshotsState.screenshots.length) % screenshotsState.screenshots.length
        );
    };

    useEffect(() => {
        const hasChanges = isDirty || charactersState.hasChanges || weaponsState.hasChanges;
        setIsSaveDisabled(!hasChanges);
    }, [isDirty, charactersState.hasChanges, weaponsState.hasChanges]);

    useEffect(() => {
        const loadData = async () => {
            setIsLoading(true);
            try {
                const [charsRes, weaponsRes, screenshotsRes, curUserRes] = await Promise.all([
                    charactersActions.loadCharacters(),
                    weaponsActions.loadWeapons(),
                    screenshotsActions.loadScreenshots(),
                    getPlayer(nickname),
                ]);
                setCurrentUser(curUserRes?.data?.display_name || "");

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
                setIsLoading(false);
            }
        };

        loadData();
    }, [nickname]);

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
        setIsLoading(true);
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
            setIsLoading(false);
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
                            {canEdit && (
                                <div className={styles.addButtonContainer}>
                                    <Item isAddButton onAddClick={charactersActions.toggleDropdown} />
                                    {charactersState.dropdownOpen && (
                                        <div className={styles.dropdown}>
                                            {charactersState.dropdownItems.map((item, i) => (
                                                <Item
                                                    showStats={false}
                                                    key={`${item.name}${i}`}
                                                    type="character"
                                                    name={item.name}
                                                    showTrash={false}
                                                    onAddClick={() => charactersActions.handleAddItem(item)}
                                                    style={{ cursor: "pointer" }}
                                                />
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                            {isLoading
                                ? Array(10)
                                      .fill(0)
                                      .map((_, i) => <SkeletonItem key={`skeleton-${i}`} />)
                                : charactersState.displayItems.map((ch, i) => (
                                      <Item
                                          key={`${ch.name}${i}`}
                                          showTrash={canEdit}
                                          canEdit={canEdit}
                                          type="character"
                                          name={ch.name}
                                          value1={ch.value1}
                                          value2={ch.value2}
                                          onRemoveClick={() => charactersActions.handleRemoveItem(ch.name)}
                                          onValueChange={charactersActions.handleValueChange}
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
                                    value={canEdit ? user?.display_name : currentUser}
                                    id="nickname"
                                    placeholder="nickname"
                                    disabled={!canEdit}
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
                                        screenshotsState.screenshots.map((screenshot, i) => (
                                            <div key={screenshot.id} className={styles.screenshotItem}>
                                                <img
                                                    src={screenshot.url}
                                                    alt={screenshot.description || "Screenshot"}
                                                    className={styles.screenshotImage}
                                                    onClick={() => openModal(i)}
                                                    style={{ cursor: "pointer" }}
                                                />
                                                {canEdit && (
                                                    <button
                                                        onClick={() => deletePlayerScreenshotById(screenshot.id)}
                                                        className={styles.trashButton}
                                                    >
                                                        <FiTrash2 className={styles.trashIcon} />
                                                    </button>
                                                )}
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
                                {canEdit && (
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
                                )}
                                {screenshotsState.uploadError && (
                                    <div className={styles.errorText}>{screenshotsState.uploadError}</div>
                                )}
                                {screenshotsState.loadError && (
                                    <div className={styles.errorText}>{screenshotsState.loadError}</div>
                                )}
                            </div>
                        </div>
                        {canEdit && (
                            <Button
                                disabled={isSaveDisabled}
                                onClick={handleSave}
                                style={{ width: "205px", fontSize: "25px" }}
                            >
                                <Trans>save</Trans>
                            </Button>
                        )}
                    </div>
                    <div className={styles.tableContainer}>
                        <h3 className={styles.tableTitle}>
                            <Trans>WEAPONS</Trans>
                        </h3>
                        <div className={styles.playerTable}>
                            {canEdit && (
                                <div className={styles.addButtonContainer}>
                                    <Item isAddButton onAddClick={weaponsActions.toggleDropdown} />
                                    {weaponsState.dropdownOpen && (
                                        <div className={styles.dropdown}>
                                            {weaponsState.dropdownItems.map((item, i) => (
                                                <Item
                                                    showStats={false}
                                                    key={`${item.name}${i}`}
                                                    type="weapon"
                                                    name={item.name}
                                                    showTrash={false}
                                                    onAddClick={() => weaponsActions.handleAddItem(item)}
                                                    style={{ cursor: "pointer" }}
                                                />
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                            {isLoading
                                ? Array(10)
                                      .fill(0)
                                      .map((_, i) => <SkeletonItem key={`skeleton-${i}`} />)
                                : weaponsState.displayItems.map((weapon, i) => (
                                      <Item
                                          key={`${weapon.name}${i}`}
                                          showTrash={canEdit}
                                          canEdit={canEdit}
                                          type="weapon"
                                          name={weapon.name}
                                          value1={weapon.value1}
                                          value2={weapon.value2}
                                          onRemoveClick={() => weaponsActions.handleRemoveItem(weapon.name)}
                                          onValueChange={weaponsActions.handleValueChange}
                                      />
                                  ))}
                        </div>
                    </div>
                </div>
                <div>
                    <TwitchStreamers />
                </div>
            </div>
            {isModalOpen && (
                <div className={styles.modalOverlay} onClick={closeModal}>
                    <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
                        <button className={styles.modalNavLeft} onClick={prevScreenshot}>
                            ←
                        </button>
                        <img
                            src={screenshotsState.screenshots[currentScreenshotIndex].url}
                            alt="Full Screenshot"
                            className={styles.modalImage}
                        />
                        <button className={styles.modalNavRight} onClick={nextScreenshot}>
                            →
                        </button>
                        <button className={styles.modalClose} onClick={closeModal}>
                            ✕
                        </button>
                    </div>
                </div>
            )}
        </FormProvider>
    );
};

export default Player;

// 1. Вынести modal в компонент
// 2. Вынести dropdown в компонент
// 3. Вынести screenshot в компонент
