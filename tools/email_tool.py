import os
import smtplib
from email.mime.text import MIMEText

def send_email(subject: str, body: str) -> str:
    email = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")
    # Recipient is separate from the login account. The app sets
    # REPORT_EMAIL_TO from the "Send report to" field; if it is
    # empty, the report goes to the Gmail account itself.
    to = os.getenv("REPORT_EMAIL_TO", "") or email

    if not email or not password:
        raise ValueError("Missing GMAIL_USER or GMAIL_APP_PASSWORD in environment.")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email, password)
        server.send_message(msg)

    return "Email sent"
