import csv
import os
from datetime import date, timedelta
from config import CONTACTS_FILE, FOLLOW_UP_DAYS

FIELDS = [
    "email", "name", "business_name", "business_type", "city",
    "domain", "email_1_sent", "email_2_sent", "email_3_sent",
    "email_1_date", "email_2_date", "email_3_date", "replied", "unsubscribed",
]


def _load() -> list[dict]:
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save(rows: list[dict]) -> None:
    os.makedirs(os.path.dirname(CONTACTS_FILE), exist_ok=True)
    with open(CONTACTS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def already_contacted(email: str) -> bool:
    return any(row["email"] == email for row in _load())


def add_contact(email: str, name: str, business_name: str, business_type: str, city: str, domain: str) -> None:
    rows = _load()
    rows.append({
        "email": email, "name": name, "business_name": business_name,
        "business_type": business_type, "city": city, "domain": domain,
        "email_1_sent": "false", "email_2_sent": "false", "email_3_sent": "false",
        "email_1_date": "", "email_2_date": "", "email_3_date": "",
        "replied": "false", "unsubscribed": "false",
    })
    _save(rows)


def mark_sent(email: str, email_number: int) -> None:
    rows = _load()
    for row in rows:
        if row["email"] == email:
            row[f"email_{email_number}_sent"] = "true"
            row[f"email_{email_number}_date"] = str(date.today())
    _save(rows)


def mark_replied(email: str) -> None:
    rows = _load()
    for row in rows:
        if row["email"] == email:
            row["replied"] = "true"
    _save(rows)


def mark_unsubscribed(email: str) -> None:
    rows = _load()
    for row in rows:
        if row["email"] == email:
            row["unsubscribed"] = "true"
    _save(rows)


def get_followups_due() -> list[tuple[dict, int]]:
    """Return (contact, email_number) pairs where a follow-up is due today."""
    rows = _load()
    due = []
    today = date.today()

    for row in rows:
        if row["replied"] == "true" or row["unsubscribed"] == "true":
            continue

        for i, days in enumerate(FOLLOW_UP_DAYS, start=2):
            email_num = i
            if row[f"email_{email_num}_sent"] == "true":
                continue
            prev_date_str = row[f"email_{email_num - 1}_date"]
            if not prev_date_str:
                continue
            prev_date = date.fromisoformat(prev_date_str)
            if today >= prev_date + timedelta(days=days):
                due.append((row, email_num))
                break  # Only one follow-up at a time per contact

    return due
