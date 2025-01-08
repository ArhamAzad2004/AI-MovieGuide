import openai
import requests
from dotenv import load_dotenv
import os

# Load API keys from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
Movie_Api_key = os.getenv("Movie_Api_key")

# OpenAI Query Processing
def process_user_query(user_query):
    prompt = f"""
    Analyze the following query for a movie recommendation system:
    Query: "{user_query}"
    Provide intent and parameter in the format: Intent: <intent>, Parameter: <parameter>
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()


# TMDb Data Fetching
def fetch_movies_from_tmdb(intent, param=None):
    base_url = "https://api.themoviedb.org/3"
    if intent == "genre":
        genres = {"Action": 28, "Comedy": 35, "Drama": 18}  # Example genres
        genre_id = genres.get(param, None)
        if genre_id:
            endpoint = f"{base_url}/discover/movie"
            response = requests.get(endpoint, params={
                "api_key": Movie_Api_key,
                "with_genres": genre_id,
                "language": "en-US"
            })
    elif intent == "trending":
        endpoint = f"{base_url}/trending/movie/day"
        response = requests.get(endpoint, params={"api_key": Movie_Api_key})
    elif intent == "search":
        endpoint = f"{base_url}/search/movie"
        response = requests.get(endpoint, params={
            "api_key": Movie_Api_key,
            "query": param,
            "language": "en-US"
        })
    else:
        return "Invalid intent."

    if response.status_code == 200:
        return response.json()["results"][:5]  # Return top 5 results
    else:
        return f"Error: {response.status_code}"

# Example Workflow
user_query = input("Ask about movies: ")
ai_response = process_user_query(user_query)

# Parse AI Response
intent, param = ai_response.replace("Intent: ", "").replace("Parameter: ", "").split(", ")
intent, param = intent.strip().lower(), param.strip().lower()

# Fetch Movies
movies = fetch_movies_from_tmdb(intent, param)
if isinstance(movies, list):
    for movie in movies:
        print(f"Title: {movie['title']}, Release Date: {movie['release_date']}")
else:
    print(movies)