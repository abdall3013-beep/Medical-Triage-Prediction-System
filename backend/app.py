from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from datetime import datetime

from database import (
    create_database,
    insert_patient,
    get_all_patients,
    delete_patient,
    clear_database
)

app = Flask(__name__)
CORS(app)

create_database()

# ===============================
# Load Model
# ===============================

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


# ===============================
# Recommendation
# ===============================

def get_recommendation(level):

    if level == 3:
        return (
            "HIGH",
            "Immediate medical assessment. Patient should NOT wait. Notify emergency physician immediately."
        )

    elif level == 2:
        return (
            "MEDIUM",
            "Patient can wait for a short period. Continuous reassessment is recommended."
        )

    else:
        return (
            "LOW",
            "Patient can wait according to the waiting queue. Routine monitoring."
        )


# ===============================
# Home
# ===============================

@app.route("/")
def home():

    return jsonify({

        "message": "Medical Triage Prediction API",

        "status": "Running"

    })


# ===============================
# Predict
# ===============================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        patient = pd.DataFrame([{

            "age": data["age"],

            "heart_rate": data["heart_rate"],

            "systolic_blood_pressure": data["systolic_blood_pressure"],

            "oxygen_saturation": data["oxygen_saturation"],

            "body_temperature": data["body_temperature"],

            "pain_level": data["pain_level"],

            "chronic_disease_count": data["chronic_disease_count"],

            "previous_er_visits": data["previous_er_visits"],

            "arrival_mode": data["arrival_mode"]

        }])

        patient = scaler.transform(patient)

        prediction = int(model.predict(patient)[0])

        confidence = None

        if hasattr(model, "predict_proba"):

            confidence = round(

                float(max(model.predict_proba(patient)[0])) * 100,

                2

            )

        priority, recommendation = get_recommendation(prediction)
        patient_data = {

            "age": data["age"],
            "heart_rate": data["heart_rate"],
            "systolic_blood_pressure": data["systolic_blood_pressure"],
            "oxygen_saturation": data["oxygen_saturation"],
            "body_temperature": data["body_temperature"],
            "pain_level": data["pain_level"],
            "chronic_disease_count": data["chronic_disease_count"],
            "previous_er_visits": data["previous_er_visits"],
            "arrival_mode": data["arrival_mode"],
            "prediction": prediction,
            "priority": priority,
            "recommendation": recommendation

        }

        insert_patient(patient_data)

        return jsonify({

            "prediction": prediction,
            "priority": priority,
            "recommendation": recommendation,
            "confidence": confidence,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# ===============================
# History APIs
# ===============================

@app.route("/history", methods=["GET"])
def history():

    return jsonify(get_all_patients())


@app.route("/history/<int:id>", methods=["DELETE"])
def delete(id):

    delete_patient(id)

    return jsonify({

        "message": "Deleted"

    })


@app.route("/history", methods=["DELETE"])
def clear():

    clear_database()

    return jsonify({

        "message": "Database Cleared"

    })


# ===============================
# Run Server
# ===============================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )