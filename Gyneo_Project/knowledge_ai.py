import os
from difflib import SequenceMatcher

# Note: sentence_transformers has heavy dependencies that slow down startup
# We'll use basic text matching instead for better performance
MODEL = None

# -------------------------------------------------------------------------
# 🩺 Knowledge Base for Gynecological Conditions
# -------------------------------------------------------------------------
GYNE_KNOWLEDGE = {
    "PCOS": {
        "causes": [
            "Hormonal imbalance, particularly elevated androgens.",
            "Insulin resistance affecting ovulation.",
            "Genetic predisposition from family history."
        ],
        "symptoms": [
            "Irregular periods", "Weight gain", "Acne", "Hair loss", "Difficulty conceiving"
        ],
        "preventions": [
            "Maintain a healthy diet and body weight.",
            "Exercise regularly to improve insulin sensitivity.",
            "Avoid excessive sugar and processed foods."
        ],
        "medicines": [
            "Metformin for insulin regulation.",
            "Oral contraceptives to balance hormones.",
            "Clomiphene citrate for inducing ovulation."
        ]
    },

    "Ovarian Cancer": {
        "causes": [
            "Genetic mutations (BRCA1 and BRCA2).",
            "Postmenopausal hormone therapy.",
            "Family history of breast or ovarian cancer."
        ],
        "symptoms": [
            "Abdominal bloating", "Pelvic pain", "Fatigue", "Weight loss", "Urinary urgency"
        ],
        "preventions": [
            "Regular pelvic examinations.",
            "Healthy lifestyle with antioxidant-rich diet.",
            "Avoid prolonged hormone therapy."
        ],
        "medicines": [
            "Carboplatin and Paclitaxel (chemotherapy).",
            "Bevacizumab for targeted therapy.",
            "Olaparib for BRCA-mutated cases."
        ]
    }, 
}

# -------------------------------------------------------------------------
# 🔍 Helper Functions: NLP-based Insights (lightweight, no heavy deps)
# -------------------------------------------------------------------------

def get_similarity_score(text1, text2):
    """Calculate basic text similarity."""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def get_most_similar_condition(query):
    """
    Find the most semantically similar disease name to the user query.
    Uses lightweight string matching for fast startup.
    """
    conditions = list(GYNE_KNOWLEDGE.keys())
    
    best_match = conditions[0]
    best_score = 0

    for condition in conditions:
        score = get_similarity_score(query, condition)
        if score > best_score:
            best_score = score
            best_match = condition
    
    return best_match, best_score


def get_insights_by_disease(disease_name):
    """
    Fetch detailed causes, preventions, and medicines for a specific condition.
    """
    disease = disease_name.strip().title()
    if disease in GYNE_KNOWLEDGE:
        return GYNE_KNOWLEDGE[disease]
    else:
        match, confidence = get_most_similar_condition(disease_name)
        result = GYNE_KNOWLEDGE[match].copy()
        result["matched_condition"] = match
        result["confidence"] = confidence
        return result


def get_insights_by_symptoms(symptom_text):
    """
    Identify the most relevant disease based on symptom description.
    """
    match, confidence = get_most_similar_condition(symptom_text)
    insights = GYNE_KNOWLEDGE[match].copy()
    insights["matched_condition"] = match
    insights["confidence"] = round(confidence * 100, 2)
    return insights


# -------------------------------------------------------------------------
# 🧠 Chatbot Response Function (ADDED — FIXES IMPORT ERROR)
# -------------------------------------------------------------------------

def get_chatbot_response(user_message):
    """
    Lightweight rule-based chatbot.
    This avoids heavy ML models and gives instant responses.
    """

    msg = user_message.lower()

    # Greetings
    if "hello" in msg or "hi" in msg:
        return "Hello! How can I assist you today?"

    # PCOS conversations
    if "pcos" in msg:
        return ("PCOS commonly causes irregular periods, acne, hair loss, and weight gain. "
                "Ask me about symptoms, prevention, treatment, or medicines.")

    # Menstrual cycle
    if "period" in msg or "menstrual" in msg or "cycle" in msg:
        return ("A normal menstrual cycle ranges from 21–35 days. "
                "Irregular cycles may be linked to PCOS or hormonal issues.")

    # Ovarian Cancer
    if "cancer" in msg:
        return ("Ovarian cancer symptoms include bloating, pelvic pain, early satiety, "
                "and weight loss. Regular screening is important.")

    # Automatically detect symptoms (smart)
    if any(word in msg for word in ["pain", "acne", "bloating", "burning", "fatigue", "hair loss"]):
        insights = get_insights_by_symptoms(user_message)
        return (
            f"Based on your symptoms, you may be referring to **{insights['matched_condition']}**.\n"
            f"Typical symptoms: {', '.join(insights['symptoms'])}\n"
            f"Suggested medicines: {', '.join(insights['medicines'])}"
        )

    # Default fallback
    return "I'm here to help! You can ask me about symptoms, diseases, treatments, reports, or prevention tips."


# -------------------------------------------------------------------------
# Simple test runner (optional)
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("Testing AI knowledge engine...\n")
    test_symptom = "irregular periods and acne"
    insights = get_insights_by_symptoms(test_symptom)
    print(f"🩺 Matched: {insights['matched_condition']}")
    print(f"⚠ Causes: {insights['causes']}")
