from flask import Flask, request, jsonify, send_from_directory, session
from models.models import db, WorkoutPlan, DietPlan, MotivationalQuote, User
from routes.auth import auth
from flask_cors import CORS
import random

app = Flask(__name__, static_folder="frontend", static_url_path="")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key"

db.init_app(app)
CORS(app)  # Ensure CORS is initialized AFTER configurations

app.register_blueprint(auth, url_prefix='/auth')

# Ensure tables are created only once, not on every request
with app.app_context():
    db.create_all()

@app.route('/')
def serve_frontend():
    return send_from_directory("frontend", "index.html")

@app.route('/plans/generate', methods=['POST'])
def generate_plans():
    user_id = session.get('user_id') or request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    goal = request.json.get('goal')
    if not goal:
        return jsonify({"error": "Goal is required"}), 400

    workouts = {
        "Weight Loss": ["Cardio", "HIIT", "Circuit Training"],
        "Muscle Gain": ["Strength Training", "Powerlifting", "Bodybuilding"],
        "Maintenance": ["Balanced Training", "Yoga", "Light Cardio"]
    }
    diets = {
        "Weight Loss": ["Low Carb", "High Protein", "Intermittent Fasting"],
        "Muscle Gain": ["High Protein", "Caloric Surplus", "Balanced Meals"],
        "Maintenance": ["Balanced Diet", "Moderate Portions", "Whole Foods"]
    }

    WorkoutPlan.query.filter_by(user_id=user_id).delete()
    DietPlan.query.filter_by(user_id=user_id).delete()

    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
        new_workout = WorkoutPlan(user_id=user_id, day_of_week=day, workout_routine=random.choice(workouts.get(goal, ["General Fitness"])))
        new_diet = DietPlan(user_id=user_id, day_of_week=day, diet_routine=random.choice(diets.get(goal, ["Balanced Diet"])))

        db.session.add(new_workout)
        db.session.add(new_diet)

    db.session.commit()
    return jsonify({"message": "Plans generated successfully!"})

@app.route('/plans/retrieve', methods=['GET'])
def retrieve_plans():
    user_id = session.get('user_id') or request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    workout_plans = WorkoutPlan.query.filter_by(user_id=user_id).all()
    diet_plans = DietPlan.query.filter_by(user_id=user_id).all()

    response = {
        "workout_plans": [{"day_of_week": plan.day_of_week, "workout_routine": plan.workout_routine} for plan in workout_plans],
        "diet_plans": [{"day_of_week": plan.day_of_week, "diet_routine": plan.diet_routine} for plan in diet_plans]
    }

    return jsonify(response), 200

@app.route('/debug/session', methods=['GET'])
def debug_session():
    return jsonify({"user_id": session.get('user_id')}), 200

if __name__ == "__main__":
    app.run(debug=True)
