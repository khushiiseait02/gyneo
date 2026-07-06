📸 Dashboard Preview


Dashboard Overview

The dashboard provides users with a centralized view of their reproductive health. It displays menstrual cycle information, health statistics, genetic risk analysis, doctor's notes, and AI-powered recommendations in a clean and interactive interface.

🔐 Login Page
<p align="center"> <img src="screenshots/login.png" width="850" alt="Login Page"> </p>

The login system securely authenticates users before allowing access to personal health records. Passwords are encrypted, and user sessions are securely managed.

👤 Registration Page
<p align="center"> <img src="screenshots/register.png" width="850" alt="Registration Page"> </p>

New users can create an account by entering their personal details. The registration process stores information securely in MongoDB.

🏥 AI Disease Prediction
<p align="center"> <img src="screenshots/upload_scan.png" width="850" alt="Upload Scan"> </p>

Users can upload medical images such as:

Ultrasound Scans
MRI Images
Cervical Images

The uploaded image is processed using a CNN/ResNet deep learning model to predict possible gynecological diseases.

📊 Prediction Result
<p align="center"> <img src="screenshots/prediction.png" width="850" alt="Prediction Result"> </p>

The AI model provides:

Predicted Disease
Confidence Score
Medical Recommendation
Risk Level

This assists healthcare professionals in making faster preliminary assessments.

🩺 Symptom Checker
<p align="center"> <img src="screenshots/symptom_checker.png" width="850" alt="Symptom Checker"> </p>

The Symptom Checker allows users to describe their symptoms in natural language.

Example:

"I have irregular periods, pelvic pain, and severe cramps."

The NLP engine extracts symptoms, compares them with trained disease patterns, and predicts possible conditions.

📅 Menstrual Cycle Tracker
<p align="center"> <img src="screenshots/cycle_tracker.png" width="850" alt="Cycle Tracker"> </p>

The menstrual cycle tracker predicts:

Current Cycle Phase
Fertile Window
Ovulation Period
Next Period Date
Remaining Days

Users can also log daily symptoms and moods for improved prediction accuracy.

🧬 Genetic Risk Assessment
<p align="center"> <img src="screenshots/genetic_risk.png" width="850" alt="Genetic Risk"> </p>

Based on family history and lifestyle information, the Genetic Risk module estimates the probability of inherited gynecological diseases and provides preventive recommendations.

🤖 AI Health Chatbot
<p align="center"> <img src="screenshots/chatbot.png" width="850" alt="Health Chatbot"> </p>

The integrated AI chatbot answers common healthcare questions related to:

PCOS
Ovarian Cancer
Menstrual Health
Fertility
Lifestyle
Nutrition
🗄️ Database Architecture
<p align="center"> <img src="screenshots/database.png" width="850" alt="Database"> </p>

MongoDB stores:

User Accounts
Medical Reports
Prediction History
Menstrual Records
Genetic Risk Reports
🧠 AI Workflow
<p align="center"> <img src="screenshots/workflow.png" width="900" alt="Workflow"> </p>
User Uploads Medical Image
            │
            ▼
 Image Preprocessing
            │
            ▼
 Feature Extraction
            │
            ▼
 CNN / ResNet Model
            │
            ▼
 Disease Prediction
            │
            ▼
 Recommendation Engine
            │
            ▼
 Dashboard Display
🏗️ System Architecture
<p align="center"> <img src="screenshots/architecture.png" width="950" alt="Architecture"> </p>
                    User
                      │
                      ▼
               Flask Application
                      │
      ┌───────────────┼──────────────┐
      ▼               ▼              ▼
 Authentication  Dashboard   Symptom Checker
      │               │              │
      ▼               ▼              ▼
 MongoDB        AI Prediction     NLP Engine
                      │
                      ▼
              CNN / ResNet Model
                      │
                      ▼
             Disease Prediction
                      │
                      ▼
          Personalized Recommendation
📈 Future Enhancements
<p align="center"> <img src="screenshots/future_scope.png" width="900" alt="Future Scope"> </p>

Planned enhancements include:

📱 Mobile Application
☁️ Cloud Deployment
🩺 Doctor Consultation Portal
📅 Appointment Booking
🎙️ Voice Assistant
⌚ Wearable Device Integration
🧾 Electronic Health Record (EHR) Support
📁 Suggested GitHub Folder Structure
GyneCare/
│
├── screenshots/
│   ├── dashboard.png
│   ├── login.png
│   ├── register.png
│   ├── upload_scan.png
│   ├── prediction.png
│   ├── chatbot.png
│   ├── cycle_tracker.png
│   ├── symptom_checker.png
│   ├── genetic_risk.png
│   ├── architecture.png
│   ├── workflow.png
│   ├── database.png
│   └── future_scope.png
│
├── static/
├── templates/
├── app.py
├── requirements.txt
└── README.md
Tip for your repository

Use your own project screenshots instead of placeholders. For architecture and workflow diagrams, create clean visuals using draw.io, Lucidchart, Canva, or Figma. This makes your repository look much more professional and helps reviewers quickly understand your project.
