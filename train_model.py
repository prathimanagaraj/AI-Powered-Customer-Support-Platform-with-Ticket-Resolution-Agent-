import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Training dataset
data = {
    "text": [
        # VPN Access
        "VPN is not connecting",
        "Unable to access company VPN",
        "VPN connection keeps failing",
        "Cannot login to VPN",
        "VPN stopped working",
        "Remote VPN connection is not available",
        "I cannot connect to the office VPN",
        "VPN authentication failed",
        "VPN disconnects frequently",
        "Unable to establish VPN connection",

        # Network Connectivity
        "Internet is not working",
        "Network connection is down",
        "WiFi is disconnected",
        "Unable to connect to the network",
        "Internet connection keeps dropping",
        "Network is very slow",
        "Cannot access the internet",
        "Office network is unavailable",
        "WiFi connection is not working",
        "Network connectivity problem",

        # Hardware Performance
        "My laptop is very slow",
        "Computer is running slowly",
        "System freezes frequently",
        "Laptop performance is poor",
        "Computer keeps freezing",
        "Laptop takes too long to start",
        "My computer is extremely slow",
        "System performance is bad",
        "Laptop hangs frequently",
        "Computer is not responding",

        # Account Access
        "I cannot login to my account",
        "Password reset is not working",
        "Unable to access my account",
        "Login credentials are not working",
        "My account is locked",
        "I forgot my password",
        "Cannot sign into my account",
        "Account login failed",
        "Unable to reset password",
        "My company account is inaccessible",

        # Email Issue
        "Email is not working",
        "Cannot send emails",
        "Unable to receive email",
        "Company email is down",
        "Outlook is not working",
        "Email messages are not being sent",
        "I cannot access my email",
        "Email service is unavailable",
        "Incoming emails are missing",
        "Cannot send or receive emails",

        # Software Issue
        "Software is not opening",
        "Application keeps crashing",
        "Unable to install software",
        "Program is showing an error",
        "Application is not working",
        "Software installation failed",
        "The application crashes when opened",
        "Program is giving an error",
        "Unable to launch the application",
        "Software stopped working"
    ],

    "category": (
        ["VPN Access"] * 10 +
        ["Network Connectivity"] * 10 +
        ["Hardware Performance"] * 10 +
        ["Account Access"] * 10 +
        ["Email Issue"] * 10 +
        ["Software Issue"] * 10
    )
}

df = pd.DataFrame(data)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["category"],
    test_size=0.25,
    random_state=42,
    stratify=df["category"]
)

# TF-IDF + Logistic Regression
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=2000,
        C=5
    ))
])

# Train
model.fit(X_train, y_train)

# Test
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("--------------------------------")
print("MODEL EVALUATION")
print("--------------------------------")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print(f"Accuracy: {accuracy * 100:.2f}%")
print("--------------------------------")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Train final model on the complete dataset
model.fit(df["text"], df["category"])

# Save final model
os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/ticket_classifier.pkl"
)

print("--------------------------------")
print("Final model trained successfully!")
print("Saved to: models/ticket_classifier.pkl")
print("--------------------------------")