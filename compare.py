from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
import requests
import os
import json

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

HEADERS = {
  "Content-Type": "application/json",
  "X-Goog-Api-Key": API_KEY,
  "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.priceLevel"
}

# The keys are the values the Place API sends back
# Map the keys to an integer
PRICE_MAP = {
  "PRICE_LEVEL_INEXPENSIVE": 1,
  "PRICE_LEVEL_MODERATE": 2,
  "PRICE_LEVEL_EXPENSIVE": 3,
  "PRICE_LEVEL_VERY_EXPENSIVE": 4
}

# fake reviews again for now
FAKE_REVIEWS_1 = [
    {
        "text": "Incredible service, food came out in under 10 minutes.",
        "rating": 5,
        "posted_at": "2024-03-12",
        "author": "James R."
    },
    {
        "text": "Waited over an hour, pasta was cold and staff was rude.",
        "rating": 1,
        "posted_at": "2024-03-16",
        "author": "Maria T."
    },
    {
        "text": "Lovely lunch spot, quick service and risotto was excellent.",
        "rating": 5,
        "posted_at": "2024-03-13",
        "author": "Chen L."
    }
]

FAKE_REVIEWS_2 = [
    {
        "text": "Cozy atmosphere and great wine selection. Food was decent.",
        "rating": 4,
        "posted_at": "2024-03-11",
        "author": "Sofia M."
    },
    {
        "text": "Overpriced for the portion sizes. Would not return.",
        "rating": 2,
        "posted_at": "2024-03-15",
        "author": "Derek P."
    },
    {
        "text": "Fantastic pasta and very attentive staff on a Monday night.",
        "rating": 5,
        "posted_at": "2024-03-18",
        "author": "Laura K."
    }
]



def fetch_restaurant(query):
    url = "https://places.googleapis.com/v1/places:searchText"
    payload = {"textQuery": query}
    response = request.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code != 200:
        return None
    places = response.json().get("priceLevel")
    if not places:
        return None

    place = places[0]
    raw_price = place.get("priceLevel")
    return {
        "google_place_id": place.get("id"),
        "name": place.get("displayName", {}).get("text"),
        "address": place.get("formattedAddress"),
        "price_level": PRICE_MAP.get(raw_price, 0),
        "rating": place.get("rating")
    }

