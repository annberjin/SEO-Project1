import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def insert_restaurant(google_place_id, name, address, price_level, rating):
    # only insert if the restaurant isnt already in the db
    existing = supabase.table("restaurants").select("id").eq(
        "google_place_id", google_place_id).execute()

    if existing.data:
        return existing.data[0]

    result = supabase.table("restaurants").insert({
        "google_place_id": google_place_id,
        "name": name,
        "address": address,
        "price_level": price_level,
        "rating": rating
        }).execute()

    return result.data[0]

def get_restaurant_by_google_place_id(google_place_id):
    result = supabase.table("restaurants").select("*").eq(
        "google_place_id", google_place_id).execute()

    if result.data:
        return result.data[0]
    else:
        return None

def get_all_restaurants():
    result = supabase.table("restaurants").select("*").execute()
    return result.data


def insert_reviews(restaurant_id, author, review_text, rating, posted_at):
    result = supabase.table("reviews").insert({
        "restaurant_id": restaurant_id,
        "author": author,
        "review_text": review_text,
        "rating": rating,
        "posted_at": posted_at
    }).execute()

    return result.data[0]

def get_reviews_by_restaurant(restaurant_id):
    result = supabase.table("reviews").select("*").eq(
        "restaurant_id", restaurant_id).execute()

    return result.data

def insert_analysis(restaurant_id, gemini_summary):
    # update if analysis exists already, elsewise we insert to the db
    existing = supabase.table("analysis").select("id").eq(
        "restaurant_id", restaurant_id).execute()

    if existing.data:
        result = supabase.table("analysis").update({
            "gemini_summary": gemini_summary
        }).eq("restaurant_id", restaurant_id).execute()
        return result.data[0]

    result = supabase.table("analysis").insert({
        "restaurant_id": restaurant_id,
        "gemini_summary": gemini_summary
    }).execute()

    return result.data[0]

def get_analysis_by_restaurant(restaurant_id):
    result = supabase.table("analysis").select("*").eq(
        "restaurant_id", restaurant_id).execute()

    if result.data:
        return result.data[0]
    else:
        return None
