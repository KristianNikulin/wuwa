import { useState } from "react";

import { getWeapons, getPlayerWeapons, addPlayerWeapons, deletePlayerWeapons } from "../../api";

export const useWeaponsState = (username) => {
    const [weapons, setWeapons] = useState([]);
    const [playerWeapons, setPlayerWeapons] = useState([]);
    const [itemsToAdd, setItemsToAdd] = useState([]);
    const [itemsToRemove, setItemsToRemove] = useState([]);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [dropdownItems, setDropdownItems] = useState([]);

    const loadWeapons = async () => {
        try {
            const [allWeaponsRes, playerWeaponsRes] = await Promise.all([getWeapons(), getPlayerWeapons(username)]);

            if (allWeaponsRes.success) setWeapons(allWeaponsRes.data);
            if (playerWeaponsRes.success) setPlayerWeapons(playerWeaponsRes.data);

            return {
                success: allWeaponsRes.success && playerWeaponsRes.success,
                error: allWeaponsRes.error || playerWeaponsRes.error,
            };
        } catch (err) {
            console.error("Load weapons error:", err);
            return { success: false, error: "Failed to load weapons" };
        }
    };

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
        if (!dropdownOpen) {
            const availableItems = weapons.filter(
                (weapon) =>
                    (!playerWeapons.some((pw) => pw.name === weapon.name) || itemsToRemove.includes(weapon.name)) &&
                    !itemsToAdd.includes(weapon.name)
            );
            setDropdownItems(availableItems);
        }
    };

    const handleAddItem = (item) => {
        if (itemsToRemove.includes(item.name)) {
            setItemsToRemove(itemsToRemove.filter((name) => name !== item.name));
        } else {
            setItemsToAdd([...itemsToAdd, item.name]);
        }
        setDropdownOpen(false);
    };

    const handleRemoveItem = (name) => {
        if (itemsToAdd.includes(name)) {
            setItemsToAdd(itemsToAdd.filter((n) => n !== name));
        } else {
            setItemsToRemove([...itemsToRemove, name]);
        }
    };

    const getDisplayItems = () => {
        const addedItems = itemsToAdd.map((name) => weapons.find((item) => item.name === name)).filter(Boolean);

        return [...playerWeapons.filter((item) => !itemsToRemove.includes(item.name)), ...addedItems];
    };

    const saveChanges = async () => {
        try {
            const results = await Promise.all([
                itemsToAdd.length > 0 ? addPlayerWeapons(username, itemsToAdd) : { success: true },
                itemsToRemove.length > 0 ? deletePlayerWeapons(username, itemsToRemove) : { success: true },
            ]);

            const errors = results.map((res) => (res.success ? null : res.error)).filter(Boolean);

            if (errors.length > 0) {
                return { success: false, error: errors.join(", ") };
            }

            const updatedRes = await getPlayerWeapons(username);
            if (updatedRes.success) {
                setPlayerWeapons(updatedRes.data);
                setItemsToAdd([]);
                setItemsToRemove([]);
            }

            return { success: true };
        } catch (err) {
            console.error("Save weapons error:", err);
            return { success: false, error: "Failed to save weapons" };
        }
    };

    return {
        state: {
            weapons,
            playerWeapons,
            dropdownOpen,
            dropdownItems,
            displayItems: getDisplayItems(),
            hasChanges: itemsToAdd.length || itemsToRemove.length,
        },
        actions: {
            loadWeapons,
            toggleDropdown,
            handleAddItem,
            handleRemoveItem,
            saveChanges,
        },
    };
};
