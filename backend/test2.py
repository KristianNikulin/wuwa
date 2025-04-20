import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]  # Коллекция для пользователей
IMAGE_FOLDER = os.path.join("static", "image", 'characters')


# Проверка пароля при входе
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Проверка правильности пароля
        user = users_collection.find_one({"username": username})

        if user and user["password"] == hash_password(password):
            session["username"] = username  # Сохраняем ник в сессии
            return redirect(url_for("save_data"))
        else:
            return render_template("index.html", message="Неверный ник или пароль")

    return render_template("index.html", message=None)


@app.route("/save", methods=["GET", "POST"])
def save_data():
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]
    user_data_collection = db[f"user_data_{username}"]

    if request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Нет данных"}), 400

        for item in data:
            # Преобразуем URL картинки в относительный путь
            image_url = item.get("url")
            if image_url:
                # Заменяем локальный URL на относительный путь
                corrected_url = image_url.replace("http://127.0.0.1:5000", "")
                item["url"] = corrected_url

            existing_entry = user_data_collection.find_one({"url": item["url"]})

            if existing_entry:
                # Если запись уже существует, обновляем цифры
                if existing_entry["value1"] != item["value1"] or existing_entry["value2"] != item["value2"]:
                    user_data_collection.update_one(
                        {"url": item["url"]},
                        {"$set": {"value1": item["value1"], "value2": item["value2"]}}
                    )
            else:
                # Если записи нет, вставляем новую
                user_data_collection.insert_one(item)

        return jsonify({"status": "success", "message": "Данные обновлены"}), 200

    return render_template("save.html")



# Страница для выбора пользователя и выгрузки данных
@app.route("/view", methods=["GET", "POST"])
def view():
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]

    # Получаем список пользователей
    users_list = users_collection.find({}, {"_id": 0, "username": 1})
    users = [user["username"] for user in users_list]

    if request.method == "POST":
        selected_user = request.form.get("selected_user")
        if selected_user:
            user_data_collection = db[f"user_data_{selected_user}"]
            data = list(user_data_collection.find({}, {"_id": 0}))  # Убираем _id
            return render_template("view.html", users=users, data=data, selected_user=selected_user)

    return render_template("view.html", users=users, data=None, selected_user=None)


# API для получения списка картинок
@app.route("/images")
def get_images():
    files = os.listdir(IMAGE_FOLDER)
    images = [f"/static/image/characters/{file}" for file in files if file.endswith((".png", ".jpg", ".jpeg"))]
    return jsonify(images)


# Хэширование пароля для безопасности
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == "__main__":
    app.run(debug=True)
