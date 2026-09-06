import sqlite3

DATABASE = "tickets.db"


def create_database():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            email TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            department TEXT NOT NULL,
            category TEXT,
            severity TEXT,
            priority TEXT,
            confidence REAL
        )
    """)

    conn.commit()
    conn.close()


def add_ticket(employee_name, email, title, description, department):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (employee_name, email, title, description, department)
        VALUES (?, ?, ?, ?, ?)
    """, (employee_name, email, title, description, department))

    conn.commit()

    ticket_id = cursor.lastrowid

    conn.close()

    return ticket_id
def update_ticket_prediction(ticket_id, category, severity, priority, confidence):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET category = ?,
            severity = ?,
            priority = ?,
            confidence = ?
        WHERE id = ?
    """, (
        category,
        severity,
        priority,
        confidence,
        ticket_id
    ))

    conn.commit()
    conn.close()