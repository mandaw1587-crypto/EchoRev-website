# EchoRev Email Campaign System

Send personalized AI-solution outreach emails to local businesses.

## Quick Start

### 1. Install dependencies
```bash
cd email
npm install
```

### 2. Configure your credentials
```bash
cp .env.example .env
# Edit .env with your SMTP credentials and sender info
```

**Gmail users:** Generate an [App Password](https://support.google.com/accounts/answer/185833) — do not use your regular Gmail password.

### 3. Add your contacts
Edit `contacts.csv` with real business info. The columns are:
- `owner_name` — First name of the owner/decision-maker
- `business_name` — Business name
- `business_type` — Type of business (used in email copy)
- `email` — Contact email
- `city` — Their city (used in email copy)
- `sent` / `replied` / `unsubscribed` — Managed automatically

### 4. Preview before sending
```bash
npm run preview         # preview email for first contact
node campaign.js preview 3  # preview for contact at row 3
# Opens preview.html — view it in your browser
```

### 5. Send outreach
```bash
npm run outreach
```

### 6. Send follow-ups (4+ days after outreach)
```bash
npm run followup
```

### 7. Check stats
```bash
npm run stats
```

## Email Templates

| Template | File | Purpose |
|----------|------|---------|
| Initial Outreach | `templates/outreach.html` | First cold email |
| Follow-up | `templates/followup.html` | Sent 4 days after if no reply |

## Marking Replies

When someone replies, update `contacts.csv` and set `replied=true` for that row.
This prevents them from receiving a follow-up.

## Unsubscribes

Set `unsubscribed=true` for any contact who asks to be removed. They will be
skipped in all future sends.

## Rate Limiting

The `EMAIL_DELAY_MS` setting in `.env` controls the delay between sends.
Keep it at 5–15 seconds to avoid spam filters.
