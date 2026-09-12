import joblib

MODEL_PATH = "models/ticket_classifier.pkl"

model = joblib.load(MODEL_PATH)


def classify_ticket(title, description):
    text = title + " " + description

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    return prediction, round(confidence, 2)


def predict_severity(title, description):
    text = (title + " " + description).lower()

    # High severity keywords
    high_keywords = [
        "server down",
        "system down",
        "security breach",
        "data loss",
        "all users",
        "entire system",
        "critical",
        "urgent",
        "production down"
    ]

    # Medium severity keywords
    medium_keywords = [
        "not working",
        "unable",
        "error",
        "failed",
        "cannot access",
        "slow",
        "problem",
        "issue"
    ]

    for keyword in high_keywords:
        if keyword in text:
            return "High"

    for keyword in medium_keywords:
        if keyword in text:
            return "Medium"

    return "Low"
def assign_priority(severity):
    if severity == "High":
        return "P1"
    elif severity == "Medium":
        return "P2"
    else:
        return "P4"