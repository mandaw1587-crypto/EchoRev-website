import requests
from config import BREVO_API_KEY, SENDER_EMAIL, SENDER_NAME

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def send_email(to_email: str, to_name: str, subject: str, body: str) -> bool:
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    # CAN-SPAM compliance footer appended to every email
    compliance_footer = (
        "\n\n---\n"
        f"Sent by {SENDER_NAME} | To unsubscribe, reply with 'unsubscribe' in the subject line."
    )

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "textContent": body + compliance_footer,
    }

    response = requests.post(BREVO_URL, json=payload, headers=headers, timeout=10)

    if response.status_code in (200, 201):
        return True

    print(f"[sender] Failed to send to {to_email}: {response.status_code} {response.text}")
    return False
