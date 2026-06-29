import os

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "EchoRev")

# Northern Michigan cities — rotated daily to cover the full region
CITIES = [
    "Harbor Springs, MI",
    "Petoskey, MI",
    "Charlevoix, MI",
    "Boyne City, MI",
    "East Jordan, MI",
    "Elk Rapids, MI",
    "Traverse City, MI",
    "Gaylord, MI",
    "Bellaire, MI",
    "Cadillac, MI",
    "Cheboygan, MI",
    "Rogers City, MI",
    "Alpena, MI",
    "Mancelona, MI",
    "Torch Lake, MI",
]

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

DAILY_SEND_LIMIT = 20  # Stay well under Gmail's 500/day free limit
FOLLOW_UP_DAYS = [3, 5]  # Days after Email 1 to send follow-ups

CONTACTS_FILE = "content-pipeline/email-automation/contacts.csv"
