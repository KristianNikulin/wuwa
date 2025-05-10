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
from collections import defaultdict

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
@app.route('/api/banned-characters', methods=['POST'])
def get_banned_characters():
    data = request.json
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')

    if not user1_id or not user2_id:
        return jsonify({'error': 'user1_id and user2_id are required'}), 400

    try:
        # Получаем всех персонажей обоих юзеров с rarity = 5
        user_chars = db.user_characters.find({
            'user_id': {'$in': [user1_id, user2_id]},
            'character_data.rarity': 5
        })

        # Группируем по character_id
        from collections import defaultdict
        grouped = defaultdict(dict)
        for item in user_chars:
            uid = item['user_id']
            cid = item['character_id']
            val2 = item['character_data'].get('value2', 0)
            grouped[cid][uid] = val2

        # Проверка на бан
        banned = []
        for cid, users in grouped.items():
            u1_has = user1_id in users
            u2_has = user2_id in users

            if not u1_has or not u2_has:
                banned.append(cid)
                continue

            val1 = users[user1_id]
            val2 = users[user2_id]

            # бан, если у кого-то > 2
            if val1 > 2 or val2 > 2:
                banned.append(cid)
            # бан, если один <=2, другой >2 — уже учтено выше
            # ничего не делаем, если оба <= 2

        return jsonify({'banned_characters': banned})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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


@app.route("/players/<string:player_name>", methods=["GET"])
def get_player(player_name):
    try:
        player = users_collection.find_one(
            {"status": "player", "username": player_name},
            {"display_name": 1, "username": 1, "_id": 0}
        )
        if player:
            return jsonify({"status": "success", "data": player}), 200
        else:
            return jsonify({"status": "error", "message": "Player not found"}), 404
    except PyMongoError:
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


@app.route("/player/<string:player_name>/weapons", methods=["GET", "POST", "DELETE", "PATCH"])
def user_weapons(player_name):
    try:
        # Проверка авторизации
        if request.method != "GET" and ('username' not in session or session['username'] != player_name):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        if request.method == "GET":
            # Получение оружия пользователя с полными данными
            user_weapons = list(db.user_weapons.find(
                {"user_id": player_name},
                {"_id": 0, "user_id": 0, "weapon_id": 0}
            ))

            weapons_list = [item["weapon_data"] for item in user_weapons]

            # Получаем редкости из общей коллекции оружия
            rarity_map = {}
            all_weapons_data = db.weapons.find(
                {}, {"_id": 0, "name": 1, "rarity": 1})
            for weapon in all_weapons_data:
                rarity_map[weapon["name"]] = weapon.get("rarity", 0)

            # Добавим редкость к каждому оружию пользователя (если есть)
            for weapon in weapons_list:
                weapon["rarity"] = rarity_map.get(weapon["name"], 0)

            # Сортируем по убыванию редкости
            weapons_list.sort(key=lambda w: w.get("rarity", 0), reverse=True)

            return jsonify({"status": "success", "data": weapons_list}), 200

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
                    "weapon_data": {'name': weapon_name, 'value1': 0, 'value2': 1}
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

        elif request.method == "PATCH":
            # Обновление значений оружия
            data = request.get_json()
            if not data or not isinstance(data, dict):
                return jsonify({"status": "error", "message": "Expected object with weapon updates"}), 400

            updated_weapons = []
            not_found_weapons = []

            for weapon_name, updates in data.items():
                # Проверяем, что обновления содержат нужные поля
                if not isinstance(updates, dict) or not all(key in updates for key in ['value1', 'value2']):
                    return jsonify({
                        "status": "error",
                        "message": f"Invalid updates for weapon {weapon_name}. Expected value1 and value2"
                    }), 400

                # Проверяем, есть ли такое оружие у пользователя
                existing = db.user_weapons.find_one({
                    "user_id": session['username'],
                    "weapon_id": weapon_name
                })

                if not existing:
                    not_found_weapons.append(weapon_name)
                    continue

                # Обновляем данные оружия
                db.user_weapons.update_one(
                    {
                        "user_id": session['username'],
                        "weapon_id": weapon_name
                    },
                    {
                        "$set": {
                            "weapon_data.value1": updates['value1'],
                            "weapon_data.value2": updates['value2']
                        }
                    }
                )
                updated_weapons.append(weapon_name)

            response = {
                "status": "success",
                "message": "Weapons updated",
            }

            if not updated_weapons and not_found_weapons:
                return jsonify(response), 404
            elif not_found_weapons:
                return jsonify(response), 207  # Multi-status
            return jsonify(response), 200

    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/player/<string:player_name>/characters", methods=["GET", "POST", "DELETE", "PATCH"])
def user_characters(player_name):
    try:
        # Проверка авторизации
        if request.method != "GET" and ('username' not in session or session['username'] != player_name):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        if request.method == "GET":
            # Получение персонажей пользователя с полными данными
            user_chars = list(db.user_characters.find(
                {"user_id": player_name},
                {"_id": 0, "user_id": 0, "weapon_id": 0}
            ))

            chars_list = [item["character_data"] for item in user_chars]

            return jsonify({"status": "success", "data": chars_list}), 200

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
                    "character_data": {'name': char_name, 'value1': 0, 'value2': 0}
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

        elif request.method == "PATCH":
            data = request.get_json()
            if not data or not isinstance(data, dict):
                return jsonify({"status": "error", "message": "Expected object with character updates"}), 400

            updated_chars = []
            not_found_chars = []

            for char_name, updates in data.items():
                # Проверяем, что обновления содержат нужные поля
                if not isinstance(updates, dict) or not all(key in updates for key in ['value1', 'value2']):
                    return jsonify({
                        "status": "error",
                        "message": f"Invalid updates for character {char_name}. Expected value1 and value2"
                    }), 400

                # Проверяем, есть ли такой персонаж у пользователя
                existing = db.user_characters.find_one({
                    "user_id": session['username'],
                    "character_id": char_name
                })

                if not existing:
                    not_found_chars.append(char_name)
                    continue

                # Обновляем данные персонажа
                db.user_characters.update_one(
                    {
                        "user_id": session['username'],
                        "character_id": char_name
                    },
                    {
                        "$set": {
                            "character_data.value1": updates['value1'],
                            "character_data.value2": updates['value2']
                        }
                    }
                )
                updated_chars.append(char_name)

            response = {
                "status": "success",
                "message": "Characters updated",
            }

            if not updated_chars and not_found_chars:
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
        if request.method != "GET" and ('username' not in session or session['username'] != player_name):
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


@app.route("/screenshots/<string:screenshot_id>", methods=["GET", "DELETE"])
def get_or_delete_screenshot(screenshot_id):
    try:
        if request.method == "GET":
            # Поиск скриншота
            screenshot = db.user_screenshots.find_one(
                {"_id": ObjectId(screenshot_id)},
                {"image_data": 1, "content_type": 1}
            )

            if not screenshot:
                return jsonify({"status": "error", "message": "Screenshot not found"}), 404

            # Отправка бинарных данных
            return Response(
                screenshot['image_data'],
                content_type=screenshot['content_type']
            )

        elif request.method == "DELETE":
            result = db.user_screenshots.delete_one(
                {"_id": ObjectId(screenshot_id)})

            if result.deleted_count == 0:
                return jsonify({"status": "error", "message": "Screenshot not found"}), 404

            return jsonify({"status": "success", "message": "Screenshot deleted"}), 200

    except PyMongoError:
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


@app.route("/tournaments", methods=["GET"])
def get_all_tournaments():
    try:
        tournaments = list(db.tournaments.find({}, {"_id": 0}))
        return jsonify({"status": "success", "data": tournaments}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/tournaments/active", methods=["GET"])
def get_active_tournament():
    try:
        active_tournaments = list(db.tournaments.find(
            {"active": True},
            {"_id": 0}
        ))

        if len(active_tournaments) == 0:
            return jsonify({
                "status": "error",
                "message": "No active tournament found"
            }), 404

        if len(active_tournaments) > 1:
            return jsonify({
                "status": "error",
                "message": "Multiple active tournaments found",
                "count": len(active_tournaments)
            }), 409

        return jsonify({
            "status": "success",
            "data": active_tournaments[0]
        }), 200

    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": "Database error"
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
