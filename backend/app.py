from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# -------------------------------
# 1. Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

model_path = os.path.join(PROJECT_DIR, "model", "model.pkl")
nn_path = os.path.join(PROJECT_DIR, "model", "nn.pkl")
data_path = os.path.join(PROJECT_DIR, "model", "data.pkl")
scaler_path = os.path.join(PROJECT_DIR, "model", "scaler.pkl")
model_name_path = os.path.join(PROJECT_DIR, "model", "model_name.pkl")

print("📦 Loading models from:", PROJECT_DIR)

# -------------------------------
# 2. Load Models
# -------------------------------
try:
    model = joblib.load(model_path)
    nn = joblib.load(nn_path)
    df = joblib.load(data_path)
    scaler = joblib.load(scaler_path)

    # Optional (for viva)
    if os.path.exists(model_name_path):
        model_name = joblib.load(model_name_path)
    else:
        model_name = "Best Model"

    print("✅ Models Loaded Successfully!")

except Exception as e:
    print(f"❌ Error loading models: {e}")

# -------------------------------
# 3. Home
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return "EduPredict API Running Successfully"

# -------------------------------
# 4. Prediction
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        vals = [
            float(data.get('study', 0)),
            float(data.get('attendance', 0)),
            float(data.get('past', 0)),
            float(data.get('assign', 0)),
            float(data.get('marks', 0))
        ]

        # -------------------------------
        # ML Prediction
        # -------------------------------
        features = scaler.transform([vals])
        ml_pred = model.predict(features)[0]

        # -------------------------------
        # Rule-based logic (backup)
        # -------------------------------
        rule_pass = (
            vals[0] > 8 and
            vals[1] > 60 and
            vals[2] > 60 and
            vals[3] > 15 and
            vals[4] > 60
        )

        # -------------------------------
        # Final Decision (HYBRID)
        # -------------------------------
        is_pass = bool(ml_pred) or rule_pass

        result = "PASS & ELIGIBLE FOR JOB ✅" if is_pass else "FAIL & NOT ELIGIBLE ❌"

        # -------------------------------
        # Insight
        # -------------------------------
        if is_pass:
            insight = "Candidate meets all industry benchmarks."
        else:
            insight = "Candidate needs improvement in academic performance."

        # -------------------------------
        # Dataset averages
        # -------------------------------
        dataset_avgs = [
            float(df['Study_Hours_per_Week'].mean()),
            float(df['Attendance_Rate'].mean()),
            float(df['Past_Exam_Scores'].mean()),
            float(df['Assignments'].mean()),
            float(df['Internal_Marks'].mean())
        ]

        # -------------------------------
        # Similar Students
        # -------------------------------
        dist, indices = nn.kneighbors(features)
        similar_ids = [str(df.iloc[idx]['Student_ID']) for idx in indices[0]]

        # -------------------------------
        # Response
        # -------------------------------
        return jsonify({
            "result": result,
            "is_pass": is_pass,
            "insight": insight,
            "model_used": model_name,
            "your_data": vals,
            "avg_data": dataset_avgs,
            "similar_ids": similar_ids
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------------------
# 5. At-Risk Students
# -------------------------------
@app.route("/at-risk", methods=["GET"])
def get_at_risk():
    try:
        risk_df = df[
            (df['Attendance_Rate'] < 60) |
            (df['Internal_Marks'] < 60)
        ].head(10)

        risk_list = [
            {
                "id": str(row['Student_ID']),
                "attendance": float(row['Attendance_Rate'])
            }
            for _, row in risk_df.iterrows()
        ]

        return jsonify(risk_list)

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------------------
# 6. Run
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)