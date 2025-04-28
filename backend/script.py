import os
import bcrypt
from pymongo import MongoClient
from pymongo.errors import PyMongoError, OperationFailure
from urllib.parse import quote_plus
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.connected = False

    def get_mongo_uri(self):
        """Формирует URI для подключения к MongoDB"""
        username = quote_plus(os.getenv('MONGO_USER', 'root'))
        password = quote_plus(os.getenv('MONGO_PASS', 'example'))
        host = os.getenv('MONGO_HOST', 'localhost')
        port = os.getenv('MONGO_PORT', '27017')
        auth_db = os.getenv('MONGO_AUTH_DB', 'admin')

        return f"mongodb://{username}:{password}@{host}:{port}/{auth_db}?authSource=admin&retryWrites=true&w=majority"

    def connect(self):
        """Устанавливает соединение с MongoDB"""
        try:
            self.client = MongoClient(
                self.get_mongo_uri(),
                serverSelectionTimeoutMS=5000,
                socketTimeoutMS=3000,
                connectTimeoutMS=3000
            )
            # Проверка подключения
            self.client.server_info()
            self.connected = True
            logger.info("Successfully connected to MongoDB")
            return True
        except PyMongoError as e:
            logger.error(f"Connection error: {e}")
            return False

    def get_database(self, db_name=None):
        """Возвращает объект базы данных"""
        if not self.connected:
            if not self.connect():
                raise RuntimeError("Cannot connect to MongoDB")

        db_name = db_name or os.getenv('MONGO_DB', 'mydatabase')
        self.db = self.client[db_name]
        return self.db

    def initialize_collections(self):
        """Инициализирует коллекции и индексы"""
        if not self.connected:
            self.get_database()

        collections = {
            "users": [
                ("username", {"unique": True}),
                ("display_name", {})
            ],
            "characters": [
                ("name", {})
            ],
            "weapons": [
                ("name", {})
            ]
        }

        for col_name, indexes in collections.items():
            try:
                # Создаем коллекции
                if col_name not in self.db.list_collection_names():
                    self.db.command("create", col_name)
                    logger.info(f"Created collection: {col_name}")

                # Создаем индексы
                col = self.db[col_name]
                for field, options in indexes:
                    col.create_index([(field, 1)], **options)
                    logger.info(f"Created index on {field} for {col_name}")

            except OperationFailure as e:
                if "already exists" not in str(e):
                    logger.warning(
                        f"Could not create collection/index for {col_name}: {e}")

    def create_initial_users(self):
        if not self.connected:
            self.get_database()

        users_collection = self.db.users

        try:
            if users_collection.count_documents({}) > 0:
                logger.info("Users collection already has data")
                return False

            users_data = [
                {
                    "username": "user1",
                    "password": hash_password("1"),
                    "display_name": "Player 1",
                    "status": "player"
                },
                {
                    "username": "admin",
                    "password": hash_password("admin123"),
                    "display_name": "Administrator",
                    "status": "admin"
                }
            ]

            result = users_collection.insert_many(users_data)
            logger.info(f"Inserted {len(result.inserted_ids)} default users")
            return True
        except PyMongoError as e:
            logger.error(f"Failed to insert users: {e}")
            return False


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def main():
    try:
        logger.info("Starting MongoDB initialization...")

        mongo_manager = MongoDBManager()
        db = mongo_manager.get_database()

        if not mongo_manager.connected:
            raise RuntimeError("Failed to connect to MongoDB")

        mongo_manager.initialize_collections()
        mongo_manager.create_initial_users()

        logger.info("Database initialization completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Initialization failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())
