# 🌸 GyneCare
## AI-Powered Gynecological Disease Diagnosis Expert System

<div align="center">

### "Empowering Women's Healthcare Through Artificial Intelligence"

GyneCare is an intelligent healthcare platform designed to assist women in the early detection of gynecological diseases using Artificial Intelligence, Deep Learning, Medical Image Analysis, and Predictive Healthcare technologies.

</div>

---

# 📖 About the Project

Gynecological diseases such as **Polycystic Ovary Syndrome (PCOS), Ovarian Cancer, Cervical Cancer, Uterine Disorders, and other reproductive health conditions** affect millions of women worldwide. Early diagnosis is often delayed due to lack of awareness, limited access to specialists, and insufficient healthcare facilities.

**GyneCare** aims to bridge this gap by providing an AI-powered healthcare platform that assists users in monitoring their reproductive health. The application combines machine learning, deep learning, medical image analysis, and health tracking into a single integrated system.

Instead of replacing doctors, the system acts as an intelligent decision-support tool that helps users understand potential health risks, monitor menstrual health, analyze symptoms, assess genetic risks, and receive preliminary disease predictions.

---

# 🎯 Problem Statement

Many women experience delayed diagnosis of gynecological diseases because:

- Limited awareness about symptoms
- Lack of specialist availability in rural areas
- Manual analysis of medical scans consumes time
- Difficulty tracking long-term reproductive health
- Limited access to personalized healthcare guidance

This project addresses these challenges by integrating AI-based disease prediction with health monitoring and personalized recommendations.

---

# 🎯 Objectives

The primary objectives of GyneCare are:

- Detect gynecological diseases at an early stage using AI.
- Assist doctors by providing preliminary image analysis.
- Enable women to monitor menstrual and reproductive health.
- Predict disease risks using machine learning models.
- Provide personalized healthcare recommendations.
- Improve healthcare accessibility through a web-based platform.
- Encourage preventive healthcare practices.

---

# 💡 Key Features

## 🔐 1. Secure User Authentication

The system provides a secure authentication mechanism where users can register and log in safely.

### Features

- User Registration
- Secure Login
- Password Encryption
- Session Management
- User Dashboard

---

## 🏥 2. AI-Based Disease Diagnosis

One of the core features of GyneCare is automated disease prediction from medical images.

Users can upload medical scans such as:

- Ultrasound Images
- MRI Scans
- Cervical Images

The uploaded image undergoes preprocessing before being passed to a Deep Learning model.

The system predicts diseases including:

- Polycystic Ovary Syndrome (PCOS)
- Ovarian Cancer
- Cervical Cancer
- Uterine Disorders

The prediction result includes:

- Predicted Disease
- Confidence Score
- Medical Recommendation

---

## 🧠 3. Deep Learning Model

The disease prediction module is powered using Convolutional Neural Networks (CNN) and ResNet architecture.

### Workflow

Medical Image

⬇

Image Preprocessing

⬇

Feature Extraction

⬇

CNN / ResNet Model

⬇

Disease Prediction

⬇

Recommendation Generation

This approach improves prediction accuracy while reducing manual diagnosis time.

---

## 🩺 4. Intelligent Symptom Checker

Users can describe their symptoms in natural language.

Example:

"I have irregular periods, pelvic pain and weight gain."

The NLP module extracts meaningful medical symptoms and compares them with trained disease patterns.

The system then predicts possible conditions and recommends whether medical consultation is necessary.

---

## 📅 5. Menstrual Cycle Tracker

The menstrual cycle module helps users monitor reproductive health.

It predicts:

- Current Cycle Phase
- Ovulation Window
- Fertile Period
- Next Menstrual Date
- Remaining Days

Users can also log symptoms, moods, and cycle history for more personalized predictions.

---

## 🧬 6. Genetic Risk Assessment

This module estimates inherited disease risks based on:

- Family Medical History
- Lifestyle
- Age
- Personal Health Information

The system calculates:

- Risk Score
- Risk Level
- Personalized Preventive Suggestions

---

## 📊 7. Personalized Health Dashboard

The dashboard acts as the central control panel for users.

It displays:

- Current Health Status
- Disease Prediction History
- Menstrual Cycle Status
- Fertility Window
- Genetic Risk Score
- Doctor's Notes
- AI Recommendations

The dashboard is designed to provide a complete overview of the user's reproductive health.

---

## 🤖 8. AI Health Chatbot

The integrated chatbot assists users by answering healthcare-related questions.

It can provide information regarding:

- Diseases
- Symptoms
- Lifestyle Improvements
- Nutrition
- Preventive Care
- Medical Guidance

The chatbot offers educational support but does not replace professional medical advice.

---

## 🌍 9. Multi-Language Support

To improve accessibility, the application supports multiple languages, enabling users from different regions to interact comfortably with the platform.

---

# ⚙️ System Architecture

```
                    User
                      │
                      ▼
          Flask Web Application
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Authentication   Dashboard     Symptom Checker
      │               │               │
      ▼               ▼               ▼
 MongoDB Database   Health Data   NLP Processing
                      │
                      ▼
             Medical Image Upload
                      │
                      ▼
              Image Preprocessing
                      │
                      ▼
              CNN / ResNet Model
                      │
                      ▼
            Disease Prediction
                      │
                      ▼
         Recommendation Generation
                      │
                      ▼
              Results Dashboard
```

---

# 🛠️ Technology Stack

## Frontend

The user interface is developed using:

- HTML5
- CSS3
- JavaScript

The interface is designed to be responsive, user-friendly, and accessible.

---

## Backend

The backend is developed using **Python Flask**, which handles:

- User Authentication
- Routing
- Disease Prediction
- Database Communication
- API Integration

---

## Database

MongoDB is used to securely store:

- User Information
- Login Credentials
- Health Records
- Prediction History
- Menstrual Data

---

## Artificial Intelligence

The AI module utilizes:

- TensorFlow
- Keras
- CNN
- ResNet50
- OpenCV
- NumPy
- Pandas

These technologies perform image preprocessing, feature extraction, and disease classification.

---

# 📂 Project Structure

```
GyneCare/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload_scan.html
│   ├── chatbot.html
│   ├── symptom_checker.html
│   ├── menstrual_cycle.html
│   └── genetic_risk.html
│
├── models/
│   ├── cnn_model.h5
│   ├── resnet_model.h5
│
├── uploads/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation Guide

### Clone the repository

```bash
git clone https://github.com/yourusername/GyneCare.git
```

### Navigate to the project directory

```bash
cd GyneCare
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### Install required packages

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 🔮 Future Scope

Future enhancements planned for GyneCare include:

- Mobile application development
- Doctor consultation portal
- Appointment scheduling
- Electronic Health Record (EHR) integration
- Wearable device synchronization
- Voice-based AI assistant
- Cloud deployment
- Explainable AI for prediction transparency
- Real-time patient monitoring
- Personalized treatment recommendations

---

# 👩‍💻 Author

**Khushi Gowda**

AI Engineer | Python Full Stack Developer | Machine Learning Enthusiast | DevOps Learner

### Technical Skills

- Python
- Flask
- Django
- Machine Learning
- Deep Learning
- TensorFlow
- OpenCV
- MongoDB
- SQL
- Git & GitHub
- HTML
- CSS
- JavaScript

---

# 📜 Disclaimer

This project is developed for educational and research purposes. The AI-generated predictions are intended to assist users and healthcare professionals but should not be considered a substitute for professional medical diagnosis or treatment.

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

Your support motivates further improvements and future healthcare innovations.
