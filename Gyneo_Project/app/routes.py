# app/routes.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import cv2
from werkzeug.utils import secure_filename

# Blueprint setup
routes = Blueprint('routes', __name__)

# Try import TensorFlow/Keras
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

from knowledge_ai import get_insights_by_disease, get_chatbot_response

bp = Blueprint('routes', __name__, template_folder='templates', static_folder='static')

# -----------------------------
# MODEL SETUP
# -----------------------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'resnet_gyne_model.h5')
CLASSES = ["Normal", "PCOS", "Ovarian_Cancer"]

model = None
if TF_AVAILABLE and os.path.exists(MODEL_PATH):
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print("Error loading model:", e)

# -----------------------------
# SYMPTOM CONDITIONS
# -----------------------------
SYMPTOM_CONDITIONS = {
    "irregular periods": "PCOS",
    "weight gain": "PCOS",
    "acne": "PCOS",
    "pelvic pain": "Ovarian Cyst",
    "bloating": "Ovarian Cyst",
    "frequent urination": "UTI",
    "burning sensation": "UTI",
    "fatigue": "Anemia / Hormonal Imbalance",
    "abnormal bleeding": "Ovarian Cancer",
    "back pain": "Ovarian Cancer"
}

# -----------------------------
# MEDICAL IMAGE VALIDATION
# -----------------------------
def is_medical_scan(filepath):
    img = cv2.imread(filepath)

    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Photos have high color variation
    color_std = np.std(img)

    # Ultrasound scans have noisy texture
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.mean(edges > 0)

    if color_std > 60:
        return False

    if edge_density < 0.01:
        return False

    return True

# -----------------------------
# MEDICAL IMAGE VALIDATION
# -----------------------------
def is_medical_scan(filepath):
    # your existing simple validation
    ...
def hard_medical_gate(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    texture = gray.var()
    color_std = np.std(img)

    if h < 120 or w < 120:
        return False

    if color_std > 75:   # human / nature / animals
        return False

    if texture < 120:    # smooth photos
        return False

    return True


# -----------------------------
# ADVANCED GYNE SCAN VALIDATION
# -----------------------------
def is_gyne_scan(img_path):
    """
    Returns True if the image is likely a gynecological scan, False otherwise
    """
    img = cv2.imread(img_path)
    if img is None:
        return False

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Measure texture variance
    texture_var = gray.var()

    # Detect edges (ultrasound scans have noisy edges)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.mean(edges > 0)

    # Measure color standard deviation
    color_std = np.std(img)

    # Reject non-medical images
    if color_std > 60:       # too colorful = likely photo
        return False
    if edge_density < 0.05:  # not enough edges = likely photo
        return False
    if texture_var < 100:    # too smooth = likely photo
        return False
    return True


# -----------------------------
# ROUTES
# -----------------------------
@bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('routes.dashboard'))

@bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    context = {
        "patient_info": session.get('patient_info', {"age": 28, "weight": 65, "height": 165}),
        "next_cycle": session.get('next_cycle', "Day 14"),
        "fertile_window": session.get('fertile_window', "3 Days"),
        "symptoms_list": session.get('symptoms_list', []),
        "recommendations": session.get('recommendations', []),
        "prediction": session.get('prediction'),
        "confidence": session.get('confidence'),
        "alert": session.get('alert'),
        "filename": session.get('filename'),
        "genetic_risk": session.get('genetic_risk', 'Low (0.8%)')
    }
    return render_template('dashboard.html', **context)

@bp.route('/cycle', methods=['GET', 'POST'])
def cycle():

    if 'username' not in session:
        return redirect(url_for('auth.login'))

    result = None
    error = None

    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            weight = float(request.form['weight'])
            cycle_length = int(request.form['cycle_length'])
            last_period = request.form['last_period']

            # ❌ Invalid input check
            if age < 10 or age > 55 or weight <= 10 or cycle_length <= 0:
                error = "Invalid inputs. Please enter valid details."
                result = None  # do not show any period date
            else:
                last_date = datetime.strptime(last_period, "%Y-%m-%d")
                next_period = last_date + timedelta(days=cycle_length)
                result = next_period.strftime("%d %B %Y")

        except Exception:
            error = "Invalid inputs. Please enter valid details."
            result = None

    return render_template('cycle.html', result=result, error=error)
    
@bp.route('/symptom_checker', methods=['GET','POST'])
def symptom_checker():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        text = request.form.get('symptoms', '').lower()
        conditions = [v for k, v in SYMPTOM_CONDITIONS.items() if k in text]
        if not conditions:
            conditions = ["No clear match"]
            rec = ["Observe symptoms", "Consult gynecologist"]
        else:
            rec = ["Consult gynecologist", "Maintain healthy lifestyle"]
        session['symptoms_list'] = conditions
        session['recommendations'] = rec
        flash("Symptoms processed", "success")
        return redirect(url_for('routes.dashboard'))

    return render_template('symptom.html')

@bp.route('/upload', methods=['GET'])
def upload():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('upload_image.html')

# -----------------------------
# CHATBOT API
# -----------------------------
@bp.route('/chatbot_query', methods=['POST'])
def chatbot_query():
    if 'username' not in session:
        return jsonify({"response": "Please login to use the chatbot."})

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"response": "Please enter a message."})

    user_message = data['message']
    response = get_chatbot_response(user_message)

    return jsonify({"response": response})

# -----------------------------
# IMAGE PREDICTION
# -----------------------------
@bp.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    if not model:
        flash("AI model unavailable", "danger")
        return redirect(url_for('routes.upload'))

    file = request.files.get('file')
    if not file:
        flash("No file uploaded", "danger")
        return redirect(url_for('routes.upload'))

    upload_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static', 'uploads'
    )
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, file.filename)
    file.save(filepath)

    try:
        # STEP 1: MEDICAL IMAGE VALIDATION
        img_gray = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        if img_gray is None:
            raise ValueError("Invalid image")
        h, w = img_gray.shape
        texture = img_gray.var()
        if h < 120 or w < 120 or texture < 150:
            result = "Invalid Medical Image"
            confidence = 0
            alert = "❌ Uploaded image is not a valid gynecological scan."
            insights = {"causes": [], "preventions": [], "medicines": []}
            return render_template(
                'prediction.html',
                prediction=result,
                confidence=confidence,
                alert=alert,
                filename=file.filename,
                causes=[],
                preventions=[],
                medicines=[]
            )

        # STEP 2: PREPROCESS IMAGE
        img = image.load_img(filepath, target_size=(224, 224))
        arr = image.img_to_array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)

        # STEP 3: MODEL PREDICTION
        preds = model.predict(arr)[0]
        idx = int(np.argmax(preds))
        confidence = round(float(preds[idx]) * 100, 2)
        result = CLASSES[idx]

        # STEP 4: CONFIDENCE FILTER
        MIN_CONFIDENCE = 45
        if confidence < MIN_CONFIDENCE:
            result = "Inconclusive Result"
            alert = "⚠ Scan detected but confidence is low. Clinical confirmation required."
            insights = {
                "causes": [],
                "preventions": ["Consult gynecologist", "Repeat scan"],
                "medicines": []
            }
        else:
            insights = get_insights_by_disease(result)
            if confidence >= 80:
                alert = "⚠ High confidence result. Immediate consultation recommended."
            elif confidence >= 60:
                alert = "⚠ Moderate confidence. Medical advice suggested."
            else:
                alert = "ℹ Low confidence. Monitor symptoms."

    except Exception as e:
        print("Prediction error:", e)
        result = "Invalid Medical Image"
        confidence = 0
        alert = "❌ Unable to process image"
        insights = {"causes": [], "preventions": [], "medicines": []}

    # SAVE TO SESSION
    session['prediction'] = result
    session['confidence'] = confidence
    session['alert'] = alert
    session['filename'] = file.filename

    return render_template(
        'prediction.html',
        prediction=result,
        confidence=confidence,
        alert=alert,
        filename=file.filename,
        causes=insights.get('causes', []),
        preventions=insights.get('preventions', []),
        medicines=insights.get('medicines', [])
    )

# -----------------------------
# GENETIC RISK ROUTE
# -----------------------------
@bp.route('/genetic-risk', methods=['GET', 'POST'])
def genetic_risk():
    risk = None
    if request.method == 'POST':
        age = int(request.form['age'])
        family = request.form['family_history']
        lifestyle = request.form['lifestyle']

        score = 0
        if age > 35:
            score += 2
        if family == 'yes':
            score += 3
        if lifestyle == 'unhealthy':
            score += 2
        elif lifestyle == 'moderate':
            score += 1

        if score <= 2:
            risk = "Low Risk"
        elif score <= 4:
            risk = "Moderate Risk"
        else:
            risk = "High Risk"

    return render_template('genetic_risk.html', risk=risk)

# -----------------------------
# LOGOUT
# -----------------------------
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
