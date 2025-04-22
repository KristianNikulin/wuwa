from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
import os
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Подключение к MongoDB
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db["users"]  # Коллекция для пользователей
# Пути к папкам изображений
IMAGE_FOLDER = os.path.join("static", "image")
CHARACTER_FOLDER = os.path.join(IMAGE_FOLDER, "characters")
WEAPON_FOLDER = os.path.join(IMAGE_FOLDER, "weapons")
users_collection = db.users  # Коллекция с пользователями

current_image = "default.png"


# Храним использованные пароли
used_passwords = []


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_files():
    """ Загружает файлы в папку пользователя """
    if "username" not in session:
        return jsonify({"error": "Не авторизован"}), 401

    username = session["username"]
    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)  # Создаём папку пользователя

    uploaded_files = request.files.values()
    saved_files = []

    for file in uploaded_files:
        if file.filename == '':
            continue

        file_path = os.path.join(user_folder, file.filename)
        file.save(file_path)
        # Относительный путь
        saved_files.append(f"/uploads/{username}/{file.filename}")

    return jsonify({"message": "Файлы загружены!", "files": saved_files})


@app.route("/get_players", methods=["GET"])
def get_players():
    users = db.users.find({"status": "player"}, {"display_name": 1, "_id": 0})
    return jsonify([user["display_name"] for user in users])


@app.route("/get_characters/<nickname>", methods=["GET"])
def get_characters(nickname):
    user = db.users.find_one({"display_name": nickname}, {
                             "username": 1, "_id": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404

    username = user["username"]
    collection_name = f"user_data_{username}"
    collection = db[collection_name]

    characters = collection.find(
        {"url": {"$regex": "/static/image/characters/"}})

    result = []
    for char in characters:
        url = char["url"]
        if url.startswith("http"):
            url = url.split("/static/")[-1]
            url = "static/" + url

        result.append({
            "url": url,
            "value1": char["value1"],
            "value2": char["value2"],
            # Добавляем имя файла для сортировки
            "filename": url.split("/")[-1]
        })

    # Сортировка: сначала 5*, потом 4*, внутри групп - по алфавиту
    def sort_key(char):
        filename = char["filename"].lower()
        is_5_star = "_5" in filename or "5" in filename  # Проверяем наличие маркера 5*
        return (
            not is_5_star,  # Сначала 5* (False будет раньше True)
            filename        # Затем сортируем по имени
        )

    sorted_result = sorted(result, key=sort_key)

    # Удаляем временное поле filename из ответа
    for char in sorted_result:
        del char["filename"]

    return jsonify(sorted_result)







@app.route("/change_display_name", methods=["POST"])
def change_display_name():
    # Получаем данные из JSON-запроса
    new_display_name = request.json.get("new_display_name")

    if not new_display_name:
        return jsonify({"success": False, "message": "Новое имя не предоставлено"}), 400

    # Логика обновления имени пользователя в базе данных
    user = users_collection.find_one({"username": session["username"]})

    if user:
        result = users_collection.update_one(
            {"username": session["username"]},
            {"$set": {"display_name": new_display_name}}
        )

        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Имя успешно обновлено!"}), 200
        else:
            return jsonify({"success": False, "message": "Ошибка обновления имени"}), 500
    else:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 404





@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Поля не заполнены"}), 400

    user = db.users.find_one({"username": username})

    if not user or user.get("password") != password:
        return jsonify({"status": "error", "message": "Неверный логин или пароль"}), 404

    # Успешный вход
    session["username"] = username
    session["status"] = user.get("status", "player")

    return jsonify({"status": "success", "message": "Вход выполнен"}), 200






# API для получения списка картинок
@app.route("/images")
def get_images():
    if not os.path.exists(CHARACTER_FOLDER):
        return jsonify([])

    files = os.listdir(CHARACTER_FOLDER)
    images = [file for file in files if file.endswith(
        (".png", ".jpg", ".jpeg"))]

    # Сортировка: сначала 5*, потом 4*, внутри групп - по алфавиту
    def sort_key(filename):
        filename_lower = filename.lower()
        # Проверяем наличие маркера 5*
        is_5_star = "_5" in filename_lower or "5" in filename_lower
        return (
            not is_5_star,  # Сначала 5* (False будет раньше True)
            filename_lower  # Затем сортируем по имени
        )

    sorted_images = sorted(images, key=sort_key)

    # Формируем полные пути после сортировки
    result = [f"/static/image/characters/{file}" for file in sorted_images]

    return jsonify(result)


@app.route("/images_weapon")
def get_images_weapon():
    if not os.path.exists(WEAPON_FOLDER):
        return jsonify([])

    files = os.listdir(WEAPON_FOLDER)

    # Получаем только изображения из папки WEAPON_FOLDER
    images = [
        f"/static/image/weapons/{file}"
        for file in files
        # Убедитесь, что это изображения
        if file.endswith((".png", ".jpg", ".jpeg"))
    ]

    return jsonify(images)


@app.route("/load_weapon", methods=["GET"])
def load_data():
    if "username" not in session or session.get("status") not in ["player", "admin"]:
        return jsonify({"status": "error", "message": "User not authenticated"}), 403

    username = session["username"]
    user_data_collection = db[f"user_data_{username}"]

    # Получаем все данные для текущего пользователя
    user_data = list(user_data_collection.find())

    # Фильтрация данных по типу
    weapon_data = [
        {"url": item["url"], "value1": item["value1"],
            "value2": item["value2"]}
        for item in user_data if "weapons" in item["url"]
    ]

    return jsonify({"status": "success", "data": weapon_data})


@app.route("/load_charakter", methods=["GET"])
def load_data2():
    if "username" not in session or session.get("status") not in ["player", "admin"]:
        return jsonify({"status": "error", "message": "User not authenticated"}), 403

    username = session["username"]
    user_data_collection = db[f"user_data_{username}"]

    # Получаем все данные для текущего пользователя
    user_data = list(user_data_collection.find())

    # Фильтрация данных по типу
    characters_data = [
        {"url": item["url"], "value1": item["value1"],
            "value2": item["value2"]}
        for item in user_data if "characters" in item["url"]
    ]

    return jsonify({"status": "success", "data": characters_data})


# Хэширование пароля для безопасности
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.before_request
def before_request():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())





@app.route('/set_players', methods=['POST'])
def set_players():
    data = request.json
    session['player1'] = data.get('players', {}).get('player1')
    session['player2'] = data.get('players', {}).get('player2')
    session['selected_indexes'] = data.get('selectedIndexes', [])
    return jsonify({'status': 'success'})


@app.route("/clear_players", methods=["POST"])
def clear_players():
    session.pop("player1", None)
    session.pop("player2", None)
    return {"status": "ok"}


@app.route('/get_session_players')
def get_session_players():
    return jsonify({
        'player1': session.get('player1'),
        'player2': session.get('player2'),
        'selected_indexes': session.get('selected_indexes', [])
    })


@app.route("/logout")
def logout():
    session.pop("status", None)
    session.pop("username", None)
    return redirect(url_for("index"))


@socketio.on('join_session')
def handle_join_session(data):
    join_room(data['session_id'])
    emit('connection_response', {'status': 'joined'})


@socketio.on('player_selected')
def handle_player_selected(data):
    emit('update_player', data, room=data['session_id'], include_self=False)


@socketio.on('character_added')
def handle_character_added(data):
    emit('update_character', data, room=data['session_id'], include_self=False)


@socketio.on('test_ping')
def handle_test_ping(data):
    emit('test_pong', data)


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
