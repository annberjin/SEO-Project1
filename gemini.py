import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# using ai generated data for now since we still need to implement the reviews endpoint
fake_reviews = [
    {
        "text": "Incredible service, food came out in under 10 minutes. "
                "Staff was attentive and friendly the whole time.",
        "rating": 5,
        "posted_at": "2024-03-12",  # Tuesday
        "author": "James R."
    },
    {
        "text": "Waited over an hour for our food on a Saturday night. "
                "Server was nowhere to be found and the pasta was cold.",
        "rating": 1,
        "posted_at": "2024-03-16",  # Saturday
        "author": "Maria T."
    },
    {
        "text": "Lovely lunch spot on a Wednesday afternoon. "
                "Quick service and the risotto was excellent.",
        "rating": 5,
        "posted_at": "2024-03-13",  # Wednesday
        "author": "Chen L."
    },
    {
        "text": "Went on a Friday evening and the place was chaotic. "
                "Staff seemed overwhelmed, took 45 minutes just for bread.",
        "rating": 2,
        "posted_at": "2024-03-15",  # Friday
        "author": "Sofia M."
    },
    {
        "text": "Sunday brunch was a disaster. Wrong orders, "
                "rude staff, and overpriced for the quality.",
        "rating": 1,
        "posted_at": "2024-03-17",  # Sunday
        "author": "Derek P."
    }
]

def analyze_reviews(reviews=None):
    if reviews is None:
        reviews = fake_reviews

    review_parts = []
    for index, review in enumerate(reviews):
        line = "Review" + str(index + 1) + " by " + review["author"] + " "
        line = line + "(posted: " + review["posted_at"] + ", rating: " + str(review["rating"]) + "/5):\n"
        line = line + review["text"]
        review_parts.append(line)

    formatted_reviews = "\n".join(review_parts)
    prompt = (
        "You are a restaurant review analyst. "
        "Given the following reviews, identify any inconsistencies "
        "or contradictions between them. Pay attention to patterns "
        "such as whether negative reviews tend to occur on weekends "
        "or busy periods versus posistive reviews on weekdays. "
        "Summarize what reviewers agree and disagree on, and flag "
        "any red flags a customer should know about. "
        "Finally, give a review reliability score from 0-100 percent where "
        "90+ means reviews are very consistent and trustworthy, 70-89 means reviews "
        "are somewhat consistent and reliable, 50-69 means reviews are contradictory "
        "and unreliable, and below 50 means reviews are very contradictory and unreliable. "
        "Format your response as:\n"
        "ANALYSIS: <your analysis>\n"
        "RELIABILITY SCORE: <score>%\n"
        "REASONING: <one sentence explanation>\n\n"
        f"{formatted_reviews}" 
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=prompt
    )

    return response.text