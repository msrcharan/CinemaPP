import requests

from django.core.management.base import BaseCommand
from cinema.models import Movie, Screen, Show  # replace '...' with the actual path to your models
import requests
from datetime import datetime, timedelta
import random
import logging
from django.utils import timezone
import pytz


class Command(BaseCommand):
    
    
    help = 'Fetch movies from an external API and store them in the database'

    
    def handle(self, *args, **options):
        movie_data = fetch_movie_data()  # Assuming this returns the list of movies
    
        if len(movie_data) > 0:
            for movie_info in movie_data:
                try:
                    Movie.objects.create(
                        title=movie_info.get('title', ''),
                        director=movie_info.get('director', ['Unknown']),
                        producer=movie_info.get('producers', ['Unknown']),
                        cast=movie_info.get('cast', []),
                        description=movie_info.get('overview', ''),
                        release_date=movie_info.get('release_date', None),
                        genre=movie_info.get('genre',''),
                        rating=movie_info.get('rating',''),
                        star_rating=movie_info.get('star_rating', 0.0),
                        duration=movie_info.get('runtime', 0),  # Assuming 0 is an acceptable default
                        image=f"https://image.tmdb.org/t/p/original{movie_info.get('poster_path', '')}",
                        trailer_url=movie_info.get('trailer_url', '')  # Assuming you have a way to get the trailer URL
                    )    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to add movie due to database error: {e}'))   

            screens = [
            {"name": "1", "capacity": 50},
            {"name": "2", "capacity": 50},
            {"name": "3", "capacity": 50},
            {"name": "4", "capacity": 50},
            {"name": "5", "capacity": 50},
            {"name": "6", "capacity": 50},
            {"name": "7", "capacity": 50},
            {"name": "8", "capacity": 50},
            {"name": "9", "capacity": 50},
            {"name": "10", "capacity": 50},
            {"name": "11", "capacity": 50},
            {"name": "12", "capacity": 50},
        ]
        for screen_data in screens:
            Screen.objects.get_or_create(name=screen_data['name'], defaults={'capacity': screen_data['capacity']})

        # Assume movies are already populated
        movies = Movie.objects.all()
        screens = Screen.objects.all()
        i = 1
        naive_datetime = datetime.now()  # Naive
        aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.timezone('America/New_York'))
        # Example of creating shows
        if movies and screens:
            for movie in movies:
                date = 1
                for screen in screens:
                    start_time = aware_datetime + timedelta(days=date)  # Random start times
                    end_time = start_time + timedelta(minutes=movie.duration)  # Assuming a 2-hour movie

                    start_time = start_time.strftime("%Y-%m-%d %H:%M")
                    end_time = end_time.strftime("%Y-%m-%d %H:%M")
                    
                    Show.objects.create(
                        show_id=i,
                        movie=movie,
                        screen=screen,
                        start_time=start_time,
                        end_time=end_time,
                        price=random.uniform(10.00, 20.00)  # Random pricing between $10 and $20
                    )
                    i += 1
                    date += 1
            
            self.stdout.write(self.style.SUCCESS('Successfully added movies to the database.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch movie data.'))

def fetch_movie_runtime(movie_id, api_key):
    """Fetch the runtime of a single movie by its ID."""
    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    detail_response = requests.get(detail_url)
    try:
        detail_response.raise_for_status()  # Raises an exception for 4XX/5XX responses
        if detail_response.status_code == 200:
            return detail_response.json().get('runtime')
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}, URL: {detail_url}")
        return None
    return None

def fetch_movie_trailers(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    response = requests.get(url)
    trailers = []
    if response.status_code == 200:
        videos = response.json().get('results', [])
        for video in videos:
            if video['type'] == 'Trailer':
                if video['site'] == 'YouTube':
                    trailers.append(f"https://www.youtube.com/watch?v={video['key']}")
                elif video['site'] == 'Vimeo':
                    trailers.append(f"https://vimeo.com/{video['key']}")
    return trailers

def fetch_movie_data():
    movies_with_complete_data = []
    for i in range(1,5):
        if i == 2:
            continue
        api_key = "75242561ec4e1ad66b850d6e58964b36"
        url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-US&page={i}"
        response = requests.get(url)
        
        if response.status_code == 200:
            movies = response.json().get('results', [])
            for movie in movies:
                movie_id = movie['id']
                detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=releases"
                detail_response = requests.get(detail_url)
                if detail_response.status_code == 200:
                    detailed_info = detail_response.json()
                    runtime = detailed_info.get('runtime')
                    star_rating = detailed_info.get('vote_average', 0.0)  # Default to 0 if not found
                    genres = ', '.join([genre['name'] for genre in detailed_info.get('genres', [])])
                    releases = detailed_info.get('releases', {}).get('countries', [])
                    us_release = next((item for item in releases if item['iso_3166_1'] == 'US'), {})
                    rating = us_release.get('certification', '')
                    if len(rating) == 0:
                        rating = 'NR'
                    trailers = fetch_movie_trailers(movie_id, api_key)
                    trailer_url = convert_youtube_link_to_embed(trailers[0]) if trailers else ' '
                    director = []
                    producers = []
                    cast = []
                    director, producers, cast = fetch_movie_details(movie_id, api_key)
                    director = ", ".join(director) if director else "Unknown"
                    producers = ", ".join(producers) if producers else "Unknown"
                    cast = ", ".join(cast) if cast else "Unknown"
                    movie.update({
                        'runtime': runtime,
                        'genre': genres,
                        'rating': rating,
                        'trailer_url': trailer_url,
                        'star_rating': star_rating,
                        'director' : director,
                        'producers' : producers,
                        'cast' : cast
                    })
                    if not any(m['id'] == movie_id for m in movies_with_complete_data):
                        movies_with_complete_data.append(movie)
        else:
            return None
    for i in range(1,2):
        api_key = "75242561ec4e1ad66b850d6e58964b36"
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={i}"
        response = requests.get(url)
        
        if response.status_code == 200:
            movies = response.json().get('results', [])
            for movie in movies:
                movie_id = movie['id']
                detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=releases"
                detail_response = requests.get(detail_url)
                if detail_response.status_code == 200:
                    detailed_info = detail_response.json()
                    runtime = detailed_info.get('runtime')
                    star_rating = detailed_info.get('vote_average', 0.0)  # Default to 0 if not found
                    genres = ', '.join([genre['name'] for genre in detailed_info.get('genres', [])])
                    releases = detailed_info.get('releases', {}).get('countries', [])
                    us_release = next((item for item in releases if item['iso_3166_1'] == 'US'), {})
                    rating = us_release.get('certification', '')
                    if len(rating) == 0:
                        rating = 'NR'
                    trailers = fetch_movie_trailers(movie_id, api_key)
                    trailer_url = convert_youtube_link_to_embed(trailers[0]) if trailers else ' '
                    
                    director, producers, cast = fetch_movie_details(movie_id, api_key)
                    director = ", ".join(director) if director else "Unknown"
                    producers = ", ".join(producers) if producers else "Unknown"
                    cast = ", ".join(cast) if cast else "Unknown"
                    movie.update({
                        'runtime': runtime,
                        'genre': genres,
                        'rating': rating,
                        'trailer_url': trailer_url,
                        'star_rating': star_rating,
                        'director' : director,
                        'producers' : producers,
                        'cast' : cast
                    })
                    if not any(m['id'] == movie_id for m in movies_with_complete_data):
                        movies_with_complete_data.append(movie)
        else:
            return None
    return movies_with_complete_data
    
    
def convert_youtube_link_to_embed(url):
    if "youtube.com/watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return url  # Return the original URL if it doesn't match expected patterns

def fetch_movie_details(movie_id, api_key):
    """Fetch the detailed information of a movie, including credits."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': api_key,
        'append_to_response': 'credits'  # Append credits to the response to get director, cast, producer
    }
    response = requests.get(url, params=params)
    credits = response.json().get('credits', [])
    
    director = [person['name'] for person in credits['crew'] if person['job'] == 'Director'][:1]
    producers = [person['name'] for person in credits['crew'] if person['job'] == 'Producer'][:3]
    cast = [person['name'] for person in credits['cast'][:5]]  # Fetch top 5 cast members for brevity
    return director, producers, cast