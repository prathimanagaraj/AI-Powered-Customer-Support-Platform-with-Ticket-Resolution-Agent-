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


app = Flask(__name__)

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

    # Make sure user is logged in
    if "logged_in" not in session:
        return redirect("/login")

    employee_name = request.form["employee_name"]
    email = request.form["email"]
    title = request.form["title"]
    description = request.form["description"]
    department = request.form["department"]


    # =====================================================
    # AI CLASSIFICATION
    # =====================================================

    category, confidence = classify_ticket(
        title,
        description
    )


    # =====================================================
    # SEVERITY
    # =====================================================

    severity = predict_severity(
        title,
        description
    )


    # =====================================================
    # PRIORITY
    # =====================================================

    priority = assign_priority(
        severity
    )


    # =====================================================
    # SAVE TICKET
    # =====================================================

    ticket_id = add_ticket(
        employee_name,
        email,
        title,
        description,
        department
    )


    # =====================================================
    # SAVE AI RESULTS
    # =====================================================

    update_ticket_prediction(
        ticket_id,
        category,
        severity,
        priority,
        confidence
    )


    # =====================================================
    # MILESTONE 2 - RAG PIPELINE
    # =====================================================

    rag_result = run_rag_pipeline(
        title,
        description
    )


    # =====================================================
    # SHOW RESULT PAGE
    # =====================================================

    return render_template(
        "result.html",

        ticket_id=ticket_id,

        employee_name=employee_name,

        category=category,

        confidence=confidence,

        severity=severity,

        priority=priority,

        rag_result=rag_result
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
