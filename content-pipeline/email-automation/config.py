import os

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "EchoRev")

CITY = os.getenv("TARGET_CITY", "Your City, State")

BUSINESS_TYPES = [
    "restaurant",
    "hair salon",
    "gym",
    "real estate agent",
    "dental clinic",
    "auto repair shop",
    "law firm",
    "accounting firm",
    "plumber",
    "electrician",
]

DAILY_SEND_LIMIT = 20  # Stay well under Brevo's 300/day free limit
FOLLOW_UP_DAYS = [3, 5]  # Days after Email 1 to send follow-ups

CONTACTS_FILE = "content-pipeline/email-automation/contacts.csv"
