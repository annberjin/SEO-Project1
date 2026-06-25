# Restaurant Reviewer
A Flask web app that helps users discover restaurants and quickly understand their quality by analyzing customer reviews. Users can search for restaurants and instantly receive summaries of common positives, negatives, and contradictions in reviews, along with an analysis of how well those reviews align with the restaurant’s overall rating.

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
Create a `.env` file in the root directory and add the following environment variables:

```env
GOOGLE_API_KEY=your_google_places_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Running the App
```bash
python search.py
```
Then open your browser and go to `http://127.0.0.1:5000`.

## Technologies Used
- Python
- Flask
- Supabase
- Google Places API
- Gemini AI
