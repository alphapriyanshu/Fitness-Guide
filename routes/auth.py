from flask import Blueprint, request, jsonify, session
from models.models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    goal = data.get('goal')

    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(name=name, email=email, goal=goal)
    new_user.set_password(password)  # Hash the password before saving

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):  # Use check_password
        return jsonify({"error": "Invalid credentials"}), 401

    session['user_id'] = user.id
    session.permanent = True  # Keep the session active

    return jsonify({"message": "Login successful", "user_id": user.id}), 200

@auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200
