from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")

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

@app.route("/")
def home():
  return jsonify({"message": "API is running"})

@app.route("/search")
def search_restaurants():
  query = request.args.get("query")
  budget = request.args.get("budget")

  if not query:
    return jsonify({"error": "Missing query"}), 400

  try:
    budget_level = int(budget)
  except:
    budget_level = 4
  
  url = "https://places.googleapis.com/v1/places:searchText"

  payload = {"textQuery": query}

  response = requests.post(url, headers=HEADERS, data=json.dumps(payload))

  if response.status_code != 200:
    return jsonify({"details": response.text}), 500

  data = response.json()

  results = []

  for place in data.get("places", []):
    raw_price = place.get("priceLevel")
    price_level = PRICE_MAP.get(raw_price, 0)

    
    # Filters out places greater than the budget
    if price_level > budget_level:
      continue

    results.append({
      "place_id": place.get("id"),
      "name": place.get("displayName", {}).get("text"),
      "address": place.get("formattedAddress"),
      "price_level": price_level,
      "rating": place.get("rating")
    })
  
  """
  Example call:
  
  GET: /search?query=italian%20food%20manhattan&budget=2
  
  output:
  [
    {
      "address": "200 W 44th St, New York, NY 10036, USA",
      "name": "Carmine's - Time Square",
      "place_id": "ChIJR9So-lRYwokRX1xEjA0rChA",
      "price_level": 2,
      "rating": 4.5
    },
    ...
  ]
  """
  
  return jsonify(results)

if __name__ == "__main__":
  app.run(debug=True)