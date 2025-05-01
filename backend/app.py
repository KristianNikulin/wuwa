import io
from bson import Binary
import base64
from werkzeug.utils import secure_filename
import bcrypt
from datetime import timedelta
from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

app = Flask(__name__)

# Конфигурация
app.config.update(
    SECRET_KEY='your-secret-key-here',
    MONGO_DB='mydatabase',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_REFRESH_EACH_REQUEST=True
)

# Конфигурация для изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# CORS
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

# Подключение к MongoDB
try:
    client = MongoClient(
        'mongodb://root:example@localhost:27017/',
        authSource='admin'
    )
    db = client[app.config['MONGO_DB']]
    users_collection = db.users
    characters_collection = db.characters
    weapons_collection = db.weapons
except PyMongoError as e:
    print(f"Database connection failed: {str(e)}")
    exit(1)


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(hashed, password):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# API Endpoints


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"status": "error", "message": "Username and password required"}), 400

        user = users_collection.find_one({"username": username})
        if not user or not check_password(user.get("password"), password):
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

        session.permanent = True
        session["username"] = username
        session["status"] = user.get("status", "player")
        session["_fresh"] = True

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "username": username,
                "display_name": user.get("display_name"),
                "status": session["status"]
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@app.route("/logout", methods=["POST"])
def logout():
    try:
        username = session["username"]
        session.clear()
        return jsonify({"status": "success", "message": "Logged out"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@app.route("/check_session", methods=["GET"])
def check_session():
    try:
        if "username" in session:
            username = session["username"]
            user = users_collection.find_one({"username": username})
            if user:
                return jsonify({
                    "status": "success",
                    "is_logged_in": True,
                    "user": {
                        "username": username,
                        "display_name": user.get("display_name"),
                        "status": session.get("status", "player")
                    }
                }), 200

        return jsonify({
            "status": "success",
            "is_logged_in": False,
            "user": None
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@app.route("/players", methods=["GET"])
def get_players():
    try:
        players = list(users_collection.find(
            {"status": "player"},
            {"display_name": 1, "username": 1, "_id": 0}
        ))
        return jsonify({"status": "success", "data": players}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/characters", methods=["GET"])
def get_characters():
    try:
        characters = list(characters_collection.find({}, {"_id": 0}))
        return jsonify({"status": "success", "data": characters}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/weapons", methods=["GET"])
def get_weapons():
    try:
        weapons = list(weapons_collection.find({}, {"_id": 0}))
        return jsonify({"status": "success", "data": weapons}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/player/<string:player_name>/weapons", methods=["GET", "POST", "DELETE"])
def user_weapons(player_name):
    try:
        # Проверка авторизации
        if 'username' not in session or session['username'] != player_name:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        if request.method == "GET":
            # Получение оружия пользователя с полными данными
            user_weapons = list(db.user_weapons.find(
                {"user_id": session['username']},
                {"_id": 0, "user_id": 0}
            ))

            # Получаем полные данные оружия из коллекции weapons
            weapons_data = []
            for uw in user_weapons:
                weapon = db.weapons.find_one(
                    {"name": uw["weapon_id"]}, {"_id": 0})
                if weapon:
                    weapons_data.append(weapon)

            return jsonify({"status": "success", "data": weapons_data}), 200

        elif request.method == "POST":
            # Добавление нового оружия (массивом)
            data = request.get_json()
            if not data or not isinstance(data.get('weapons'), list):
                return jsonify({"status": "error", "message": "Expected array of weapons"}), 400

            added_weapons = []
            skipped_weapons = []

            for weapon_name in data['weapons']:
                # Проверка существования оружия
                weapon = db.weapons.find_one({"name": weapon_name}, {"_id": 0})
                if not weapon:
                    skipped_weapons.append(weapon_name)
                    continue

                # Проверяем, есть ли уже такое оружие у пользователя
                existing = db.user_weapons.find_one({
                    "user_id": session['username'],
                    "weapon_id": weapon_name
                })

                if existing:
                    skipped_weapons.append(weapon_name)
                    continue

                # Добавление связи
                db.user_weapons.insert_one({
                    "user_id": session['username'],
                    "weapon_id": weapon_name,
                    "weapon_data": weapon  # Сохраняем полные данные оружия
                })
                added_weapons.append(weapon_name)

            response = {
                "status": "success",
                "message": "Weapons added",
            }

            if not added_weapons and skipped_weapons:
                return jsonify(response), 207  # Multi-status
            return jsonify(response), 200

        elif request.method == "DELETE":
            # Удаление оружия из коллекции пользователя
            data = request.get_json()
            if not data or not isinstance(data.get('weapons'), list):
                return jsonify({"status": "error", "message": "Expected array of weapons"}), 400

            deleted_weapons = []
            not_found_weapons = []

            for weapon_name in data['weapons']:
                # Удаляем связь пользователя с оружием
                result = db.user_weapons.delete_one({
                    "user_id": session['username'],
                    "weapon_id": weapon_name
                })

                if result.deleted_count > 0:
                    deleted_weapons.append(weapon_name)
                else:
                    not_found_weapons.append(weapon_name)

            response = {
                "status": "success",
                "message": "Weapons deleted",
                "deleted": deleted_weapons,
                "not_found": not_found_weapons
            }

            if not deleted_weapons and not_found_weapons:
                return jsonify(response), 404
            elif not_found_weapons:
                return jsonify(response), 207  # Multi-status
            return jsonify(response), 200

    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/player/<string:player_name>/characters", methods=["GET", "POST", "DELETE"])
def user_characters(player_name):
    try:
        # Проверка авторизации
        if 'username' not in session or session['username'] != player_name:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        if request.method == "GET":
            # Получение персонажей пользователя с полными данными
            user_chars = list(db.user_characters.find(
                {"user_id": session['username']},
                {"_id": 0, "user_id": 0}
            ))

            # Получаем полные данные персонажей из коллекции characters
            chars_data = []
            for uc in user_chars:
                character = db.characters.find_one(
                    {"name": uc["character_id"]}, {"_id": 0})
                if character:
                    chars_data.append(character)

            return jsonify({"status": "success", "data": chars_data}), 200

        elif request.method == "POST":
            # Добавление новых персонажей (массивом)
            data = request.get_json()
            if not data or not isinstance(data.get('characters'), list):
                return jsonify({"status": "error", "message": "Expected array of characters"}), 400

            added_chars = []
            skipped_chars = []

            for char_name in data['characters']:
                # Проверка существования персонажа
                character = db.characters.find_one(
                    {"name": char_name}, {"_id": 0})
                if not character:
                    skipped_chars.append(char_name)
                    continue

                # Проверяем, есть ли уже такой персонаж у пользователя
                existing = db.user_characters.find_one({
                    "user_id": session['username'],
                    "character_id": char_name
                })

                if existing:
                    skipped_chars.append(char_name)
                    continue

                # Добавление связи
                db.user_characters.insert_one({
                    "user_id": session['username'],
                    "character_id": char_name,
                    "character_data": character  # Сохраняем полные данные персонажа
                })
                added_chars.append(char_name)

            response = {
                "status": "success",
                "message": "Characters added",
            }

            if not added_chars and skipped_chars:
                return jsonify(response), 207  # Multi-status
            return jsonify(response), 200

        elif request.method == "DELETE":
            # Удаление персонажей из коллекции пользователя
            data = request.get_json()
            if not data or not isinstance(data.get('characters'), list):
                return jsonify({"status": "error", "message": "Expected array of characters"}), 400

            deleted_chars = []
            not_found_chars = []

            for char_name in data['characters']:
                # Удаляем связь пользователя с персонажем
                result = db.user_characters.delete_one({
                    "user_id": session['username'],
                    "character_id": char_name
                })

                if result.deleted_count > 0:
                    deleted_chars.append(char_name)
                else:
                    not_found_chars.append(char_name)

            response = {
                "status": "success",
                "message": "Characters deleted",
                "deleted": deleted_chars,
                "not_found": not_found_chars
            }

            if not deleted_chars and not_found_chars:
                return jsonify(response), 404
            elif not_found_chars:
                return jsonify(response), 207  # Multi-status
            return jsonify(response), 200

    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/player/<string:player_name>/screenshots", methods=["GET", "POST", "DELETE"])
def user_screenshots(player_name):
    try:
        # Проверка авторизации
        if 'username' not in session or session['username'] != player_name:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        if request.method == "GET":
            # Получаем ВСЕ данные скриншотов включая image_data
            screenshots_cursor = db.user_screenshots.find(
                {"user_id": player_name})
            screenshots = []

            for screenshot in screenshots_cursor:
                # Преобразуем бинарные данные в base64 для передачи по JSON
                image_base64 = base64.b64encode(
                    screenshot['image_data']).decode('utf-8')

                screenshots.append({
                    "id": str(screenshot['_id']),
                    "filename": screenshot['filename'],
                    "size": screenshot.get('size', 0),
                    "content_type": screenshot.get('content_type', 'image/png'),
                    "image_data": image_base64  # Бинарные данные в base64
                })

            return jsonify({
                "status": "success",
                "data": screenshots,
                "count": len(screenshots)
            }), 200

        elif request.method == "POST":
            # Проверка наличия файла
            if 'file' not in request.files:
                return jsonify({"status": "error", "message": "No file uploaded"}), 400

            file = request.files['file']

            # Проверка расширения файла
            if not allowed_file(file.filename):
                return jsonify({"status": "error", "message": "Invalid file type"}), 400

            # Проверка размера файла
            file.seek(0, io.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_FILE_SIZE:
                return jsonify({"status": "error", "message": "File too large"}), 400

            # Проверяем, существует ли уже файл с таким именем у этого пользователя
            existing_file = db.user_screenshots.find_one({
                "user_id": session['username'],
                "filename": secure_filename(file.filename)
            })

            if existing_file:
                return jsonify({
                    "status": "error",
                    "message": "File with this name already exists"
                }), 409

            # Чтение файла в бинарном формате
            binary_data = Binary(file.read())

            # Определение content type
            content_type = file.content_type or 'application/octet-stream'

            # Сохранение в MongoDB
            result = db.user_screenshots.insert_one({
                "user_id": session['username'],
                "filename": secure_filename(file.filename),
                "image_data": binary_data,
                "size": file_size,
                "content_type": content_type
            })

            return jsonify({
                "status": "success",
                "message": "Screenshot uploaded",
                "id": str(result.inserted_id),
                "filename": secure_filename(file.filename),
                "size": file_size
            }), 201

        elif request.method == "DELETE":
            # Проверка наличия ID скриншота
            if 'screenshot_id' not in request.json:
                return jsonify({"status": "error", "message": "No screenshot ID provided"}), 400

            screenshot_id = request.json['screenshot_id']

            # Удаление скриншота
            result = db.user_screenshots.delete_one({
                "_id": ObjectId(screenshot_id),
                "user_id": session['username']
            })

            if result.deleted_count == 0:
                return jsonify({"status": "error", "message": "Screenshot not found or not owned by user"}), 404

            return jsonify({"status": "success", "message": "Screenshot deleted"}), 200

    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/screenshots/<string:screenshot_id>", methods=["GET"])
def get_screenshot(screenshot_id):
    try:
        # Поиск скриншота
        screenshot = db.user_screenshots.find_one(
            {"_id": ObjectId(screenshot_id)},
            {"image_data": 1, "content_type": 1}
        )

        if not screenshot:
            return jsonify({"status": "error", "message": "Screenshot not found"}), 404

        # Отправка бинарных данных
        from flask import Response
        return Response(
            screenshot['image_data'],
            content_type=screenshot['content_type']
        )

    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/player/name", methods=["POST"])
def change_display_name():
    try:
        new_name = request.json.get("newDisplayName")
        if not new_name or len(new_name) < 3:
            return jsonify({"status": "error", "message": "Invalid display name"}), 400

        username = session["username"]
        result = users_collection.update_one(
            {"username": username},
            {"$set": {"display_name": new_name}}
        )

        if result.modified_count > 0:
            return jsonify({"status": "success", "message": "Display name updated"}), 200
        else:
            return jsonify({"status": "error", "message": "Update failed"}), 400

    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
