import anthropic
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a cold email copywriter for EchoRev. You write 3-email outreach sequences
targeting local business owners to sell them AI-powered services (automation, AI chatbots, AI marketing,
AI content creation).

Rules:
- Never open with "I" — open with them and their world
- No buzzwords: no "synergy", "leverage", "revolutionary", "game-changer"
- Sound like a human, not a marketing department
- One ask per email, never two
- Subject lines under 50 characters, no spam words
- Short and direct — busy business owners delete long emails

Output ONLY valid JSON in this exact format, no markdown, no extra text:
{
  "email_1": {
    "subject": "...",
    "body": "..."
  },
  "email_2": {
    "subject": "...",
    "body": "..."
  },
  "email_3": {
    "subject": "...",
    "body": "..."
  }
}

Email 1 (5-7 sentences): Cold intro. Open with their world. One problem you solve. One result/proof point. Soft CTA — a question or low-friction next step.
Email 2 (3-5 sentences, Day 3): Brief reference to Email 1. New angle or stat. Ask if they're the right person.
Email 3 (2-3 sentences, Day 5): Short. Direct. Give them an easy out while keeping the door open.

Use these placeholders exactly as written: {{FIRST_NAME}}, {{BUSINESS_NAME}}, {{CITY}}"""


def generate_email_sequence(business_name: str, business_type: str, city: str) -> dict:
    prompt = f"""Generate a 3-email cold outreach sequence for this local business:

Business name: {business_name}
Business type: {business_type}
City: {city}

The service being pitched: AI tools and automation that save them time and help them get more customers
(e.g. AI chatbot for their website, automated follow-up texts, AI-written social media posts).

Personalise the pain points to a {business_type} owner specifically."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    return json.loads(message.content[0].text)


def personalise(template: str, first_name: str, business_name: str, city: str) -> str:
    return (
        template
        .replace("{{FIRST_NAME}}", first_name)
        .replace("{{BUSINESS_NAME}}", business_name)
        .replace("{{CITY}}", city)
    )
