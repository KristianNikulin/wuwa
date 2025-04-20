import hashlib
from pymongo import MongoClient

# Подключение к MongoDB (замени на свой URL, если нужно)
client = MongoClient("mongodb://localhost:27017/")

# Выбираем базу данных и коллекцию
db = client["mydatabase"]
users_collection = db["users"]

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Данные пользователей
users_data = [
    # {"username": "user1", "password": hash_password("password123"), "display_name": 'user1', "statys": 'player'},
    # {"username": "user2", "password": hash_password("mypassword"), "display_name": 'user2', "statys": 'player'},
    # {"username": "user3", "password": hash_password("secretpass"), "display_name": 'user3', "statys": 'player'},
    # {"username": "user4", "password": hash_password("secretpass"), "display_name": 'user4', "statys": 'player'},
    # {"username": "admin", "password": hash_password("mysecurepassword"), "display_name": 'admin', "statys": 'admin'},




]

# Добавляем пользователей в базу данных
users_collection.insert_many(users_data)

print("Пользователи успешно добавлены в базу данных!")



