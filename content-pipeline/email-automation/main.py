"""
EchoRev Email Automation
Runs daily via GitHub Actions. Finds local businesses, generates personalised
3-email sequences with Claude, sends via Brevo, and tracks follow-ups.
"""

import random
from config import BUSINESS_TYPES, CITY, DAILY_SEND_LIMIT
from leads import search_businesses, enrich_leads
from generate import generate_email_sequence, personalise
from sender import send_email
from tracker import already_contacted, add_contact, mark_sent, get_followups_due

sent_today = 0


def send_followups() -> int:
    global sent_today
    due = get_followups_due()
    for contact, email_num in due:
        if sent_today >= DAILY_SEND_LIMIT:
            break

        sequence = generate_email_sequence(
            business_name=contact["business_name"],
            business_type=contact["business_type"],
            city=contact["city"],
        )

        email_key = f"email_{email_num}"
        subject = personalise(sequence[email_key]["subject"], contact["name"], contact["business_name"], contact["city"])
        body = personalise(sequence[email_key]["body"], contact["name"], contact["business_name"], contact["city"])

        success = send_email(contact["email"], contact["name"], subject, body)
        if success:
            mark_sent(contact["email"], email_num)
            sent_today += 1
            print(f"[followup] Email {email_num} sent to {contact['email']}")

    return sent_today


def send_new_outreach() -> int:
    global sent_today
    business_type = random.choice(BUSINESS_TYPES)
    print(f"[leads] Searching for {business_type} in {CITY}")

    raw_leads = search_businesses(business_type, CITY, max_results=30)
    leads = enrich_leads(raw_leads)
    print(f"[leads] Found {len(leads)} leads with emails")

    for lead in leads:
        if sent_today >= DAILY_SEND_LIMIT:
            print(f"[main] Daily send limit of {DAILY_SEND_LIMIT} reached")
            break

        if already_contacted(lead["email"]):
            print(f"[tracker] Skipping {lead['email']} — already contacted")
            continue

        print(f"[generate] Writing email sequence for {lead['name']}")
        try:
            sequence = generate_email_sequence(
                business_name=lead["name"],
                business_type=lead["business_type"],
                city=CITY,
            )
        except Exception as e:
            print(f"[generate] Failed for {lead['name']}: {e}")
            continue

        first_name = lead["name"].split()[0]  # Best guess at first name from business name
        subject = personalise(sequence["email_1"]["subject"], first_name, lead["name"], CITY)
        body = personalise(sequence["email_1"]["body"], first_name, lead["name"], CITY)

        success = send_email(lead["email"], lead["name"], subject, body)
        if success:
            add_contact(
                email=lead["email"],
                name=first_name,
                business_name=lead["name"],
                business_type=lead["business_type"],
                city=CITY,
                domain=lead["domain"],
            )
            mark_sent(lead["email"], 1)
            sent_today += 1
            print(f"[send] Email 1 sent to {lead['email']} ({lead['name']})")

    return sent_today


if __name__ == "__main__":
    print(f"[main] Starting daily run — target city: {CITY}")
    send_followups()
    if sent_today < DAILY_SEND_LIMIT:
        send_new_outreach()
    print(f"[main] Done. Total sent today: {sent_today}")
