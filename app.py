from flask import Flask, render_template, request, redirect, session

from database import (
    create_database,
    add_ticket,
    update_ticket_prediction
)

from classifier import (
    classify_ticket,
    predict_severity,
    assign_priority
)

from rag.pipeline import run_rag_pipeline
from agents import MultiAgentOrchestrator

app = Flask(__name__)
orchestrator = MultiAgentOrchestrator()

# Secret key for login session
app.secret_key = "supportpilot-secret-key"


# Create database when the application starts
create_database()


# =========================================================
# HOME / DASHBOARD
# =========================================================

@app.route("/")
def home():

    # If user is not logged in, go to login page
    if "logged_in" not in session:
        return redirect("/login")

    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Demo login credentials
        if username == "admin" and password == "supportpilot123":

            session["logged_in"] = True
            session["username"] = username

            return redirect("/")

        else:

            return render_template(
                "login.html",
                error="Invalid username or password."
            )

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# SUBMIT TICKET
# =========================================================

@app.route("/submit", methods=["POST"])
def submit_ticket():
    if "logged_in" not in session:
        return redirect("/login")

    employee_name = request.form["employee_name"]
    email = request.form["email"]
    title = request.form["title"]
    description = request.form["description"]
    department = request.form["department"]

    # -----------------------------
    # M1: AI Ticket Classification
    # -----------------------------
    category, confidence = classify_ticket(title, description)
    severity = predict_severity(title, description)
    priority = assign_priority(severity)

    # Store ticket in database
    ticket_id = add_ticket(
        employee_name,
        email,
        title,
        description,
        department
    )

    update_ticket_prediction(
        ticket_id,
        category,
        severity,
        priority,
        confidence
    )

    # -----------------------------
    # M2 + M3: RAG + Multi-Agent
    # -----------------------------
    rag_result = run_rag_pipeline(
        title,
        description
    )

    m3_result = orchestrator.run(
        title,
        description,
        email
    )

    # -----------------------------
    # Display result
    # -----------------------------
    return render_template(
        "result.html",
        ticket_id=ticket_id,
        employee_name=employee_name,
        category=category,
        confidence=confidence,
        severity=severity,
        priority=priority,
        rag_result=rag_result,
        m3_result=m3_result
    )
# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
