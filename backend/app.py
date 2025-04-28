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


@app.route("/user/characters", methods=["GET"])
def get_user_characters():
    try:
        username = session["username"]
        user_characters = db[f"user_{username}_characters"].find({}, {
                                                                 "_id": 0})
        return jsonify({"status": "success", "data": list(user_characters)}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/user/weapons", methods=["GET"])
def get_user_weapons():
    try:
        username = session["username"]
        user_weapons = db[f"user_{username}_weapons"].find({}, {"_id": 0})
        return jsonify({"status": "success", "data": list(user_weapons)}), 200
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error"}), 500


@app.route("/user/change_display_name", methods=["POST"])
def change_display_name():
    try:
        new_name = request.json.get("new_display_name")
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
