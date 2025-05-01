import { useState } from "react";

import { getCharacters, getPlayerCharacters, addPlayerCharacters, deletePlayerCharacters } from "../../api";

export const useCharactersState = (username) => {
    const [characters, setCharacters] = useState([]);
    const [playerCharacters, setPlayerCharacters] = useState([]);
    const [itemsToAdd, setItemsToAdd] = useState([]);
    const [itemsToRemove, setItemsToRemove] = useState([]);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [dropdownItems, setDropdownItems] = useState([]);

    const loadCharacters = async () => {
        try {
            const [allCharsRes, playerCharsRes] = await Promise.all([getCharacters(), getPlayerCharacters(username)]);

            if (allCharsRes.success) setCharacters(allCharsRes.data);
            if (playerCharsRes.success) setPlayerCharacters(playerCharsRes.data);

            return {
                success: allCharsRes.success && playerCharsRes.success,
                error: allCharsRes.error || playerCharsRes.error,
            };
        } catch (err) {
            console.error("Load characters error:", err);
            return { success: false, error: "Failed to load characters" };
        }
    };

    const toggleDropdown = () => {
        setDropdownOpen(!dropdownOpen);
        if (!dropdownOpen) {
            const availableItems = characters.filter(
                (char) =>
                    (!playerCharacters.some((pc) => pc.name === char.name) || itemsToRemove.includes(char.name)) &&
                    !itemsToAdd.includes(char.name)
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
        const addedItems = itemsToAdd.map((name) => characters.find((item) => item.name === name)).filter(Boolean);

        return [...playerCharacters.filter((item) => !itemsToRemove.includes(item.name)), ...addedItems];
    };

    const saveChanges = async () => {
        try {
            const results = await Promise.all([
                itemsToAdd.length > 0 ? addPlayerCharacters(username, itemsToAdd) : { success: true },
                itemsToRemove.length > 0 ? deletePlayerCharacters(username, itemsToRemove) : { success: true },
            ]);

            const errors = results.map((res) => (res.success ? null : res.error)).filter(Boolean);

            if (errors.length > 0) {
                return { success: false, error: errors.join(", ") };
            }

            const updatedRes = await getPlayerCharacters(username);
            if (updatedRes.success) {
                setPlayerCharacters(updatedRes.data);
                setItemsToAdd([]);
                setItemsToRemove([]);
            }

            return { success: true };
        } catch (err) {
            console.error("Save characters error:", err);
            return { success: false, error: "Failed to save characters" };
        }
    };

    return {
        state: {
            characters,
            playerCharacters,
            dropdownOpen,
            dropdownItems,
            displayItems: getDisplayItems(),
            hasChanges: itemsToAdd.length || itemsToRemove.length,
        },
        actions: {
            loadCharacters,
            toggleDropdown,
            handleAddItem,
            handleRemoveItem,
            saveChanges,
        },
    };
};
