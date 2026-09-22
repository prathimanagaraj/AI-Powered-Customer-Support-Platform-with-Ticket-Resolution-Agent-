import os
import smtplib
from email.message import EmailMessage


def send_resolution_email(
    recipient_email,
    ticket_title,
    resolution,
    confidence
):
    sender_email = os.getenv("SUPPORTPILOT_EMAIL")
    sender_password = os.getenv("SUPPORTPILOT_EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        return {
            "status": "not_configured",
            "message": "Email credentials are not configured."
        }

    message = EmailMessage()

    message["Subject"] = f"SupportPilot - Ticket Resolved: {ticket_title}"
    message["From"] = sender_email
    message["To"] = recipient_email

    message.set_content(
        f"""Hello,

Your support ticket has been analyzed by SupportPilot.

Ticket:
{ticket_title}

Resolution confidence:
{confidence}%

Troubleshooting Resolution:

{resolution}

Please follow the above steps. If the issue persists, contact the IT support team.

Regards,
SupportPilot
"""
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return {
            "status": "sent",
            "message": "Resolution email sent successfully."
        }

    except Exception as error:
        return {
            "status": "failed",
            "message": str(error)
        }