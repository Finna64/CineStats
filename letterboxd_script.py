"""
FUTURE IMPLEMENTATIONS:
- AI MOVIE RECOMMENDATION SYSTEM
- SMARTER SEARCHING FUNCTIONALITY
- COMPARISON OF YOUR RATING VS AVERAGE VIEWER RATING
- COMPARISON OF YOUR RATING VS CRITIC RATING
- RANDOMISE FROM LIST OF AVERAGE RATING RESPONSES
- FIX OMDB DIRECTOR N/A PROBLEM (J.J. ABRAMS RETURNS AS N/A)
- TOP RATED (AVERAGE FILM RATING) DIRECTOR I HAVE VIEWED
- PIE CHARTS: DIRECTORS, GENRES
- TOP WATCHED ACTORS
- WEEKS WATCHED STREAK
- GIVE ME A RANDOM MOVIE TO WATCH
- SAVE MOVIE TO CACHE
- GENRE AND DIRECTOR PROFILES BY RATING
"""

import re, requests
import json
from csv import DictReader

#OMDB API Key
API_KEY = "22b78895"

#setting up csv data
with open("/ratings.csv", "r") as file:
       ratings_rows = list(DictReader(file))

       for movie in ratings_rows:
              print(movie["Name"])

def search_movie_from_ratings():
       # OUTPUTS RATING WHEN SEARCHED FOR MOVIE TITLE
       search_term = input("Enter movie title to search...")
       for movie in ratings_rows:
              if movie[1].lower() == search_term.lower():
                     print(movie[4])

RATING_DICT = {
       "rating_level_0" : {
              "range": [0, 1],
              "response": "you can't be serious..."
       },
       "rating_level_1" : {
              "range": [1, 2],
              "response": "this guy's a hater."
       },
       "rating_level_2" : {
              "range": [2, 3],
              "response": "a little harsh, aren't ya?"
       },
       "rating_level_3" : {
              "range": [3, 4],
              "response": "you know a good movie when you see one."
       },
       "rating_level_4" : {
              "range": [4, 5],
              "response": "easy to please, hey..."
       },
}

def print_rated_list():
       # PRINTS EACH RATED MOVIE WITH RELEASE YEAR AND RATING
       for movie in ratings_rows:
              print(f"{movie["Name"]} ({movie["Year"]}) - {movie["Rating"]}")

def print_avg_rating():

       avg_rating = 0
       counter = 0
       for movie in ratings_rows:
              avg_rating += float(movie["Rating"])
              counter += 1
       avg_rating = avg_rating / counter
       avg_rating = round(avg_rating, 2)

       response = ""
       for rating_level in RATING_DICT:
              if (avg_rating >= RATING_DICT[rating_level]["range"][0] and avg_rating <= RATING_DICT[rating_level]["range"][1]):
                     response = RATING_DICT[rating_level]["response"]
              else:
                     continue

       print(f"Your average given rating is {avg_rating}, {response}")

def IMDB_rating_for_rated_movies():

       for movie in ratings_rows:
              with open("api_data.json", "r") as f:
                     cached_movies = json.load(f)
              api_data = { movie["Title"]: movie for movie in cached_movies }

              try:
                     api_row = api_data.get(movie["Name"])
                     print(f"{api_row["Title"]} ({api_row["Director"]}) Rating: {api_row["imdbRating"]}, Genre: {api_row["Genre"]}")
              except:
                     print("***** Skipping: " + movie["Name"] + " *****")
                     continue

def create_genre_profile():

       existing_genre_names = []
       all_genre_names = []

       for movie in ratings_rows:
                     response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie[1]}")
                     omdb_movie_data = response.json()
                     genre_raw_string = omdb_movie_data['Actors'] # change genre to director for director profile
                     genre_list = genre_raw_string.split(", ")
                     print(omdb_movie_data["Title"], genre_list)

                     for genre in genre_list:
                            all_genre_names.append(genre)
                            if genre not in existing_genre_names:
                                   existing_genre_names.append(genre)


       genre_view_percentage_list = [] #e.g. [['Adventure', 0.53], ['Action', 0.38], ['Drama', 0.47]]

       genre_total_count = len(all_genre_names)
       for genre in existing_genre_names:
              count_genre = all_genre_names.count(genre)
              portion = round((count_genre / genre_total_count), 4)
              genre_view_percentage_list.append([genre, count_genre])

       genre_view_percentage_list.sort(reverse = True, key = lambda genre_view_percentage_list: genre_view_percentage_list[1])
       
       # print("YOUR DIRECTOR PROFILE:")
       # for genre_portion_pair in genre_view_percentage_list[:10]:
       #        print(f"{genre_portion_pair[0]}: {round(genre_portion_pair[1] * 100)}%")

       print("YOUR ACTOR PROFILE:")
       for genre_portion_pair in genre_view_percentage_list[:10]:
              print(f"{genre_portion_pair[0]}, {genre_portion_pair[1]}")
                   
def count_actor_watches():

       actors_watches_list = []
       all_actors = []

       for movie in ratings_rows:
                            response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie[1]}")
                            omdb_movie_data = response.json()
                            print(omdb_movie_data["Title"])
                            actors_in_movie = omdb_movie_data["Actors"].split(", ")
                            for actor in actors_in_movie:
                                   
                                   if actor not in all_actors:
                                          all_actors.append(actor)
                                   

       print(all_actors)

                            # actors_in_movie = ["Timothée Chalamet", "Rebecca Ferguson", "Zendaya"]

def load_api_data():
       api_data_list = []

       for movie in ratings_rows:
              response = requests.get(
                     "https://www.omdbapi.com/",
                     params={"apikey": API_KEY, "t": movie[1]},
                     timeout=10,
                     )
              
              response.raise_for_status()
              data = response.json()

              if data.get("Response") == "True":
                     api_data_list.append(data)
                     print(f"Saving: {data['Title']}")
              else:
                     print(f"Skipping {movie[1]}: {data.get('Error')}")

       with open("api_data.json", "w", encoding="utf-8") as f:
              json.dump(api_data_list, f, indent=4, ensure_ascii=False)

# IMDB_rating_for_rated_movies()