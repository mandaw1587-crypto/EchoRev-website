import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, SENDER_NAME

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to_email: str, to_name: str, subject: str, body: str) -> bool:
    # CAN-SPAM compliance footer
    compliance_footer = (
        "\n\n---\n"
        f"Sent by {SENDER_NAME} | To unsubscribe, reply with 'unsubscribe' in the subject line."
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{GMAIL_ADDRESS}>"
    msg["To"] = to_email
    msg.attach(MIMEText(body + compliance_footer, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[sender] Failed to send to {to_email}: {e}")
        return False
