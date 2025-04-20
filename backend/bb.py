import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('site_data.db')
cursor = conn.cursor()

# Создание таблицы для пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Создание таблицы для персонажей
cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    image TEXT NOT NULL
)
''')

# Создание таблицы для оружия
cursor.execute('''
CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    image TEXT NOT NULL
)
''')

# Список пользователей
users = {
    "player1": "password1",
    "player2": "password2",
    "player3": "password3",
    "player4": "password4",
    "player5": "password5",
    "player6": "password6",
    # Добавь еще 34 игрока
}

# Добавление пользователей в таблицу
for username, password in users.items():
    cursor.execute('''
    INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, password))

# Список персонажей
characters = {
    "char1": {"name": "Aalto", "image": "static/image/characters/Aalto_Icon.png"},
    "char2": {"name": "Baizhi", "image": "static/image/characters/Baizhi_Icon.png"},
    "char3": {"name": "Brant", "image": "static/image/characters/Brant_Icon.png"},
    "char4": {"name": "Calcharo", "image": "static/image/characters/Calcharo_Icon.png"},
    "char5": {"name": "Camellya", "image": "static/image/characters/Camellya_Icon.png"},
    "char6": {"name": "Carlotta", "image": "static/image/characters/Carlotta_Icon.png"},
    "char7": {"name": "Youhu", "image": "static/image/characters/Youhu_Icon.png"},
    "char8": {"name": "Yuanwu", "image": "static/image/characters/Yuanwu_Icon.png"},
    "char9": {"name": "Zhezhi", "image": "static/image/characters/Zhezhi_Icon.png"},
    "char10": {"name": "Jianxin", "image": "static/image/characters/Jianxin_Icon.png"},
    "char11": {"name": "Changli", "image": "static/image/characters/Changli_Icon.png"},
    "char12": {"name": "Chixia", "image": "static/image/characters/Chixia_Icon.png"},
    "char13": {"name": "Lumi", "image": "static/image/characters/Lumi_Icon.png"},
    "char14": {"name": "Jinhsi", "image": "static/image/characters/Jinhsi_Icon.png"},
    "char15": {"name": "Jiyan", "image": "static/image/characters/Jiyan_Icon.png"},
    "char16": {"name": "lingyang", "image": "static/image/characters/lingyang_Icon.png"},
    "char17": {"name": "Danjin", "image": "static/image/characters/Danjin_Icon.png"},
    "char18": {"name": "Encore", "image": "static/image/characters/Encore_Icon.png"},
    "char19": {"name": "Mortefi", "image": "static/image/characters/Mortefi_Icon.png"},
    "char20": {"name": "Phoebe", "image": "static/image/characters/Phoebe_Icon.png"},
    "char21": {"name": "Roccia", "image": "static/image/characters/Roccia_Icon.png"},
    "char22": {"name": "Rover-Havoc", "image": "static/image/characters/Rover-Havoc_Icon.png"},
    "char23": {"name": "Rover-Spectro", "image": "static/image/characters/Rover-SpectroF_Icon.png"},
    "char24": {"name": "Sanhua", "image": "static/image/characters/Sanhua_Icon.png"},
    "char25": {"name": "Shorekeeper", "image": "static/image/characters/Shorekeeper_Icon.png"},
    "char26": {"name": "Taoqi", "image": "static/image/characters/Taoqi_Icon.png"},
    "char27": {"name": "Verina", "image": "static/image/characters/Verina_Icon.png"},
    "char28": {"name": "Xiangli Yao", "image": "static/image/characters/Xiangli Yao_Icon.png"},
    "char29": {"name": "Yangyang", "image": "static/image/characters/Yangyang_Icon.png"},
    "char30": {"name": "Yinlin", "image": "static/image/characters/Yinlin_Icon.png"},
}

# Добавление персонажей в таблицу
for char_id, char_data in characters.items():
    cursor.execute('''
    INSERT INTO characters (name, image) VALUES (?, ?)
    ''', (char_data["name"], char_data["image"]))

# Список оружия
weapons = {
    "char1": {"name": "3Originite Type 1", "image": "static/image/weapons/3Originite_Type_1.png"},
    "char2": {"name": "3Originite Type 2", "image": "static/image/weapons/3Originite_Type_2.png"},
    "char3": {"name": "3Originite Type4", "image": "static/image/weapons/3Originite_Type4.png"},
    "char4": {"name": "4Amity Accord", "image": "static/image/weapons/4Amity_Accord.png"},
    "char5": {"name": "4Augment", "image": "static/image/weapons/4Augment.png"},
    "char6": {"name": "4Autumntra", "image": "static/image/weapons/4Autumntra.png"},
    "char7": {"name": "4Cadenza", "image": "static/image/weapons/4Cadenza.png"},
    "char8": {"name": "4Call of the Abyss", "image": "static/image/weapons/4Call_of_the_Abyss.png"},
    "char9": {"name": "4Celestial Spiral", "image": "static/image/weapons/4Celestial_Spiral.png"},
    "char10": {"name": "4Comet Flare", "image": "static/image/weapons/4Comet_Flare.png"},
    "char11": {"name": "4Commando of Conviction", "image": "static/image/weapons/4Commando_of_Conviction.png"},
    "char12": {"name": "4Discord", "image": "static/image/weapons/4Discord.png"},
    "char13": {"name": "4Endless Collapse", "image": "static/image/weapons/4Endless_Collapse.png"},
    "char14": {"name": "4Fables of Wisdom", "image": "static/image/weapons/4Fables_of_Wisdom.png"},
    "char15": {"name": "4Fusion Accretion", "image": "static/image/weapons/4Fusion_Accretion.png"},
    "char16": {"name": "4Gauntlets#21D", "image": "static/image/weapons/4Gauntlets_21D.png"},
    "char17": {"name": "4Helios Cleaver", "image": "static/image/weapons/4Helios_Cleaver.png"},
    "char18": {"name": "4Hollow Mirage", "image": "static/image/weapons/4Hollow_Mirage.png"},
    "char19": {"name": "4Jinzhou Keeper", "image": "static/image/weapons/4Jinzhou_Keeper.png"},
    "char20": {"name": "4Legend of Drunken Hero", "image": "static/image/weapons/4Legend_of_Drunken_Hero.png"},
    "char21": {"name": "4Lumingloss", "image": "static/image/weapons/4Lumingloss.png"},
    "char22": {"name": "4Marcato", "image": "static/image/weapons/4Marcato.png"},
    "char23": {"name": "4Meditations on Mercy", "image": "static/image/weapons/4Meditations_on_Mercy.png"},
    "char24": {"name": "4Ocean's Gift", "image": "static/image/weapons/4Ocean's_Gift.png"},
    "char25": {"name": "4Overture", "image": "static/image/weapons/4Overture.png"},
    "char26": {"name": "4Rectifier#", "image": "static/image/weapons/4Rectifier_.png"},
    "char27": {"name": "4Relativistic Jet", "image": "static/image/weapons/4Relativistic_Jet.png"},
    "char28": {"name": "4Romance in Farewell", "image": "static/image/weapons/4Romance_in_Farewell.png"},
    "char29": {"name": "4Somnoire Anchor", "image": "static/image/weapons/4Somnoire_Anchor.png"},
    "char30": {"name": "4Stonard", "image": "static/image/weapons/4Stonard.png"},
    "char31": {"name": "4Sword#18", "image": "static/image/weapons/4Sword_18.png"},
    "char32": {"name": "4Undying Flame", "image": "static/image/weapons/4Undying_Flame.png"},
    "char33": {"name": "4Variation", "image": "static/image/weapons/4Variation.png"},
    "char34": {"name": "4Waltz in Masquerade", "image": "static/image/weapons/4Waltz_in_Masquerade.png"},
    "char35": {"name": "4Waning Redshift", "image": "static/image/weapons/4Waning_Redshift.png"},
    "char36": {"name": "5Abyss Surges", "image": "static/image/weapons/5Abyss_Surges.png"},
    "char37": {"name": "5Cosmic Ripples", "image": "static/image/weapons/5Cosmic_Ripples.png"},
    "char38": {"name": "5Emerald of Genesis", "image": "static/image/weapons/5Emerald_of_Genesis.png"},
    "char39": {"name": "5Lustrous Razor", "image": "static/image/weapons/5Lustrous_Razor.png"},
    "char40": {"name": "5Static Mist", "image": "static/image/weapons/5Static_Mist.png"},
    "char41": {"name": "5Ages of Harvest", "image": "static/image/weapons/5Ages_of_Harvest.png"},
    "char42": {"name": "5Blazing Brilliance", "image": "static/image/weapons/5Blazing_Brilliance.png"},
    "char43": {"name": "5Luminous Hymn", "image": "static/image/weapons/5Luminous_Hymn.png"},
    "char44": {"name": "5Red Spring", "image": "static/image/weapons/5Red_Spring.png"},
    "char45": {"name": "5Rime-Draped Sprouts", "image": "static/image/weapons/5Rime-Draped_Sprouts.png"},
    "char46": {"name": "5Stellar Symphony", "image": "static/image/weapons/5Stellar_Symphony.png"},
    "char47": {"name": "5Stringmaster", "image": "static/image/weapons/5Stringmaster.png"},
    "char48": {"name": "5The Last Dance", "image": "static/image/weapons/5The_Last_Dance.png"},
    "char49": {"name": "5Tragicomedy", "image": "static/image/weapons/5Tragicomedy.png"},
    "char50": {"name": "5Unflickering Valor", "image": "static/image/weapons/5Unflickering_Valor.png"},
    "char51": {"name": "5Verdant Summit", "image": "static/image/weapons/5Verdant_Summit.png"},
    "char52": {"name": "5Verity's Handle", "image": "static/image/weapons/5Verity's_Handle.png"},
}

# Добавление оружия в таблицу
for char_id, weapon_data in weapons.items():
    cursor.execute('''
    INSERT INTO weapons (name, image) VALUES (?, ?)
    ''', (weapon_data["name"], weapon_data["image"]))

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
conn.close()

print("База данных и данные успешно созданы и добавлены.")
