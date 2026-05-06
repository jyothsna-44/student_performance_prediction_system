# 🎓 Student Performance Prediction System

## 📌 Project Overview

The **Student Performance Prediction System** is a Machine Learning based web application that predicts whether a student is likely to pass and become job eligible based on academic performance indicators.

The project uses:

* Machine Learning model for prediction
* Flask backend API
* HTML, CSS, JavaScript frontend
* KNN model for finding similar students
* Hybrid rule-based + ML prediction approach

---

# 🚀 Features

✅ Predicts student performance

✅ Detects at-risk students

✅ Hybrid prediction system (ML + Rule Based)

✅ Displays similar student profiles

✅ Shows dataset average comparison

✅ Interactive frontend UI

---

# 🛠️ Technologies Used

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* Python
* Flask
* Flask-CORS

## Machine Learning

* Scikit-learn
* Joblib
* NumPy
* K-Nearest Neighbors (KNN)

---

# 📂 Project Structure

```bash
student_performance_project/
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── model/
│   ├── model.pkl
│   ├── nn.pkl
│   ├── scaler.pkl
│   ├── data.pkl
│   └── model_name.pkl
│
├── data/
│   └── student_data.xlsx
│
├── notebook/
│   └── model.ipynb
│
└── README.md
```

---

# 📊 Input Parameters

The model predicts performance using:

* Study Hours per Week
* Attendance Rate
* Past Exam Scores
* Assignments Score
* Internal Marks

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/jyothsna-44/student-performance-prediction-system.git
```

## 2️⃣ Navigate to Project Folder

```bash
cd student-performance-prediction-system
```

## 3️⃣ Install Dependencies

```bash
pip install flask flask-cors scikit-learn numpy pandas joblib
```

## 4️⃣ Run Backend Server

```bash
cd backend
python app.py
```

Backend runs on:

```bash
http://127.0.0.1:5000/
```

## 5️⃣ Open Frontend

Open `frontend/index.html` in browser.

---

# 🧠 Machine Learning Workflow

1. Data Collection
2. Data Preprocessing
3. Feature Scaling
4. Model Training
5. Prediction Generation
6. Similar Student Detection using KNN
7. Result Visualization

---

# 📈 Future Enhancements

* Deploy using Render/Heroku
* Add database integration
* Add authentication system
* Improve UI dashboard
* Add performance analytics charts

---

# 👩‍💻 Author

**Jyothsna R**
Computer Science Engineering Student

---

# 📜 License

This project is for educational and academic purposes.
