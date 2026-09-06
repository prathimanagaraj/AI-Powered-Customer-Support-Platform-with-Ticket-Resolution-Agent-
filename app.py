from flask import Flask, render_template, request
from database import (
    create_database,
    add_ticket,
    update_ticket_prediction
)
from classifier import (
    classify_ticket,
    predict_severity,
    assign_priority )

app = Flask(__name__)

# Create database when the application starts
create_database()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_ticket():

    employee_name = request.form["employee_name"]
    email = request.form["email"]
    title = request.form["title"]
    description = request.form["description"]
    department = request.form["department"]

    # AI classification
    category, confidence = classify_ticket(title, description)

    # Severity
    severity = predict_severity(title, description)

    # Priority
    priority = assign_priority(severity)

    # Save ticket
    ticket_id = add_ticket(
        employee_name,
        email,
        title,
        description,
        department
    )

    # Save AI results
    update_ticket_prediction(
        ticket_id,
        category,
        severity,
        priority,
        confidence
    )

    # Show the same page with AI analysis
    return render_template(
        "result.html",
        ticket_id=ticket_id,
        employee_name=employee_name,
        category=category,
        confidence=confidence,
        severity=severity,
        priority=priority
    )
if __name__ == "__main__":
    app.run(debug=True)