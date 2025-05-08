import React, { useState } from "react";
import { useAdmin } from "../../../state-providers/AdminContext";
import { usePickBansState } from "./state";

import Item from "../../../components/Item";
import SkeletonItem from "../../../components/SkeletonItem";

import styles from "./styles.module.scss";

export const PickBansStep = () => {
    const {
        nextStep,
        players: { player1, player2 },
        galograms: { player1Ban, player2Ban, player1Choose, player2Choose, random },
        games,
        updateState,
    } = useAdmin();

    const [immunityCharacters, setImmunityCharacters] = useState([]);
    const [bannedCharacters, setBannedCharacters] = useState([]);

    const [immunityDropdown, setImmunityDropdown] = useState(false);
    const [bannedDropdown, setBannedDropdown] = useState(false);

    const { player1Characters, player2Characters, uniqueCharacters, isLoading } = usePickBansState(
        player1.username,
        player2.username
    );

    const handleAddImmunity = (item) => {
        setImmunityCharacters((prev) => [...prev, item]);
        setImmunityDropdown(false);
    };

    const handleAddBanned = (item) => {
        setBannedCharacters((prev) => [...prev, item]);
        setBannedDropdown(false);
    };

    const availableImmunityCharacters = uniqueCharacters.filter(
        (ch) => !immunityCharacters.some((ic) => ic.name === ch.name)
    );

    const availableBannedCharacters = uniqueCharacters.filter(
        (ch) => !bannedCharacters.some((bc) => bc.name === ch.name)
    );

    return (
        <div className={styles.galogramsContent}>
            <div>
                <div className={styles.bans}>
                    <div>{player1.display_name}</div>
                    <div className={styles.bansContainer}>
                        <div>
                            {" "}
                            <Item
                                key={player1Ban}
                                showTrash={false}
                                canEdit={false}
                                showStats={false}
                                type="galogram"
                                name={player1Ban}
                                rarity={0}
                            />
                            <Item
                                key={123}
                                showTrash={false}
                                canEdit={false}
                                showStats={false}
                                type="galogram"
                                name={""}
                                onAddClick={() => {}}
                                rarity={0}
                            />
                        </div>
                        <h3>bans</h3>
                        <div>
                            {" "}
                            <Item
                                key={234}
                                showTrash={false}
                                canEdit={false}
                                showStats={false}
                                type="galogram"
                                name={""}
                                rarity={0}
                            />
                            <Item
                                key={player2Ban}
                                showTrash={false}
                                canEdit={false}
                                showStats={false}
                                type="galogram"
                                name={player2Ban}
                                rarity={0}
                            />
                        </div>
                    </div>
                    <div>{player2.display_name}</div>
                </div>
                <div className={styles.picks}>
                    <div>
                        <Item
                            key={player1Choose}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="galogram"
                            name={player1Choose}
                            rarity={5}
                        />
                        <Item
                            key={player1Ban}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="character"
                            name={""}
                        />
                        <Item
                            key={player1Ban}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="character"
                            name={""}
                        />
                        <Item
                            key={player1Ban}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="character"
                            name={""}
                        />
                    </div>
                    <h3>picks</h3>
                    <div>
                        <Item
                            key={player1Ban}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="character"
                            name={""}
                        />
                        <Item
                            key={player1Ban}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="character"
                            name={""}
                        />
                        <Item
                            key={player1Ban}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="character"
                            name={""}
                        />
                        <Item
                            key={player2Choose}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="galogram"
                            name={player2Choose}
                            rarity={5}
                        />
                    </div>
                </div>
                <div className={styles.game}>
                    <div>==</div>
                    <button type="button" className={styles.nextButton} onClick={nextStep}>
                        Game {games.length + 1}
                    </button>
                    <div>==</div>
                </div>
                <div className={styles.chars}>
                    <div>
                        {isLoading
                            ? Array(10)
                                  .fill(0)
                                  .map((_, i) => <SkeletonItem key={`skeleton-${i}`} />)
                            : player1Characters.map((ch, i) => (
                                  <Item
                                      key={`player1${ch.name}${i}`}
                                      showTrash={false}
                                      canEdit={false}
                                      type="character"
                                      name={ch.name}
                                      value1={ch.value1}
                                      value2={ch.value2}
                                  />
                              ))}
                    </div>
                    <div className={styles.chsrsGal}>
                        <Item
                            key={player1Choose}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="galogram"
                            name={player1Choose}
                            rarity={5}
                        />
                        <Item
                            key={player2Choose}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="galogram"
                            name={player2Choose}
                            rarity={5}
                        />
                        <Item
                            key={random}
                            showTrash={false}
                            canEdit={false}
                            showStats={false}
                            type="galogram"
                            name={random}
                            rarity={5}
                        />
                    </div>
                    <div>
                        {player2Characters.map((ch, i) => (
                            <Item
                                key={`player2${ch.name}${i}`}
                                showTrash={false}
                                canEdit={false}
                                type="character"
                                name={ch.name}
                                value1={ch.value1}
                                value2={ch.value2}
                            />
                        ))}
                    </div>
                </div>
            </div>
            <div className={styles.bottom}>
                <div>
                    <p>immunity</p>
                    <div className={styles.playerTable}>
                        <div className={styles.addButtonContainer}>
                            <Item isAddButton onAddClick={() => setImmunityDropdown((prev) => !prev)} />
                            {immunityDropdown && (
                                <div className={styles.dropdownLeft}>
                                    {availableImmunityCharacters.map((item, i) => (
                                        <Item
                                            showStats={false}
                                            key={`${item.name}${i}`}
                                            type="character"
                                            name={item.name}
                                            showTrash={false}
                                            onAddClick={() => handleAddImmunity(item)}
                                            style={{ cursor: "pointer" }}
                                        />
                                    ))}
                                </div>
                            )}
                        </div>
                        {immunityCharacters.map((ch, i) => (
                            <Item
                                key={`${ch.name}${i}`}
                                showTrash={false}
                                showStats={false}
                                canEdit={false}
                                type="character"
                                name={ch.name}
                                value1={ch.value1}
                                value2={ch.value2}
                            />
                        ))}
                    </div>
                </div>
                <div>
                    <p>bans</p>
                    <div className={styles.playerTable}>
                        {bannedCharacters.map((ch, i) => (
                            <Item
                                key={`${ch.name}${i}`}
                                showTrash={false}
                                showStats={false}
                                canEdit={false}
                                type="character"
                                name={ch.name}
                                value1={ch.value1}
                                value2={ch.value2}
                                rarity={0}
                            />
                        ))}
                        <div className={styles.addButtonContainer}>
                            <Item rarity={0} isAddButton onAddClick={() => setBannedDropdown((prev) => !prev)} />
                            {bannedDropdown && (
                                <div className={styles.dropdownRight}>
                                    {availableBannedCharacters.map((item, i) => (
                                        <Item
                                            showStats={false}
                                            key={`${item.name}${i}`}
                                            type="character"
                                            name={item.name}
                                            showTrash={false}
                                            rarity={0}
                                            onAddClick={() => handleAddBanned(item)}
                                            style={{ cursor: "pointer" }}
                                        />
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
