import time
import requests
from urllib.parse import urlparse
from config import GOOGLE_PLACES_API_KEY, HUNTER_API_KEY


def search_businesses(business_type: str, city: str, max_results: int = 10) -> list[dict]:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": f"{business_type} in {city}", "key": GOOGLE_PLACES_API_KEY}

    results = []
    while len(results) < max_results:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for place in data.get("results", []):
            results.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "place_id": place.get("place_id"),
                "business_type": business_type,
                "website": None,
                "domain": None,
                "email": None,
            })

        next_page_token = data.get("next_page_token")
        if not next_page_token or len(results) >= max_results:
            break
        time.sleep(2)  # Google requires a short delay before using next_page_token
        params = {"pagetoken": next_page_token, "key": GOOGLE_PLACES_API_KEY}

    return results[:max_results]


def get_place_website(place_id: str) -> str | None:
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "website", "key": GOOGLE_PLACES_API_KEY}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("result", {}).get("website")


def find_email_via_hunter(domain: str, company_name: str) -> str | None:
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "company": company_name,
        "api_key": HUNTER_API_KEY,
        "limit": 5,
    }
    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    emails = data.get("emails", [])

    # Prefer generic/contact emails over personal ones
    preferred_types = {"generic", "webmaster"}
    for email in emails:
        if email.get("type") in preferred_types:
            return email.get("value")

    # Fall back to first result
    if emails:
        return emails[0].get("value")

    # Last resort: try info@ if hunter found the domain is valid
    if data.get("domain"):
        return f"info@{domain}"

    return None


def enrich_leads(leads: list[dict]) -> list[dict]:
    enriched = []
    for lead in leads:
        website = get_place_website(lead["place_id"])
        if not website:
            continue

        lead["website"] = website
        domain = urlparse(website).netloc.replace("www.", "")
        lead["domain"] = domain

        email = find_email_via_hunter(domain, lead["name"])
        if not email:
            continue

        lead["email"] = email
        enriched.append(lead)
        time.sleep(0.5)  # Avoid hammering Hunter.io rate limits

    return enriched
