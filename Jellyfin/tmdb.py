import pandas as pd
import requests
from collections import defaultdict
from tqdm import tqdm
import pycountry
from concurrent.futures import ThreadPoolExecutor, as_completed
import tabulate

API_KEY = 'tmdb_api_key'
MOVIE_CSV = 'movies.csv'

columns = ['date_watched', 'title', 'year', 'url', 'rating', 'col6', 'col7', 'col8']
df = pd.read_csv(MOVIE_CSV, names=columns, header=None)
movie_titles = df['title'].tolist()

TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
headers = {'Accept': 'application/json'}

lang_movies = defaultdict(list)

def get_language_name(lang_code):
    lang = pycountry.languages.get(alpha_2=lang_code)
    return lang.name if lang else lang_code

def fetch_movie(title):
    params = {
        'api_key': API_KEY,
        'query': title,
        'include_adult': 'true',
        'page': 1
    }
    try:
        response = requests.get(TMDB_SEARCH_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                lang = data['results'][0]['original_language']
                movie_found = data['results'][0]['title']
                return lang, movie_found
        else:
            print(f"Error fetching {title}: {response.status_code}")
    except Exception as e:
        print(f"Exception for {title}: {e}")
    return None

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(fetch_movie, title): title for title in movie_titles}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing movies"):
        result = future.result()
        if result:
            lang, movie_found = result
            lang_movies[lang].append(movie_found)

# Count movies by language, convert code to name
lang_counts = [
    (get_language_name(lang), len(movies))
    for lang, movies in lang_movies.items()
]
lang_counts.sort(key=lambda x: x[1], reverse=True)

# Print ASCII table
print(tabulate.tabulate(lang_counts, headers=["Language", "Count"], tablefmt="simple"))
