from django.http import HttpResponse
from django.shortcuts import render
import os
import pandas as pd   
from django.conf import settings
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import requests

url = "https://api.themoviedb.org/3/authentication"



def home (request):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNzQzZmYzMjg0MDExMThjY2RiNTA4NjhjMjY4MjE1MiIsInN1YiI6IjY1ZDhlNjRlOWEzNThkMDE4NmZmMjA1ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Kj6TLvydffG3maZFl0Lgf8oTrA7rnALVR1AFYMbVMTY"
    }
    response = requests.get(url, headers=headers)

    print(response.text)
    return render (request, 'home.html')

def backends(request):
    moviename = "Bal"


def random_movie(request):

    csv_path = os.path.join(settings.STATIC_ROOT, 'movies.csv')
    with open(csv_path, 'r') as file:
       df = pd.read_csv(file)
    
    import random
    
    moviename_index = random.randint(1, len(df.index))
    r_movie = df[df.index==moviename_index]

    
    movie_name = r_movie['Film Name'].values[0]
   

    params = { 'moviename' : movie_name}
    return render (request, 'movierecommend.html', params)

def f_suggestion(request): 
    movie_name = None  # Initialize movie_name variable
    
    if request.method == 'POST':
        movie_name = request.POST.get('input_movie_name')
        
        csv_path = os.path.join(settings.STATIC_ROOT, 'movies.csv')
        df = pd.read_csv(csv_path)
        
        featured_columns = ['title', 'genres', 'keywords', 'cast', 'director']
        for fc in featured_columns:
            df[fc] = df[fc].fillna('')
        
        combined_features = df['title'] + ' ' + df['genres'] + ' ' + df['keywords'] + ' ' + df['cast'] + ' ' + df['director']
        
        vectorizer = TfidfVectorizer()
        feature_vector = vectorizer.fit_transform(combined_features)
        similarity = cosine_similarity(feature_vector)
        
        list_of_all_titles = df['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        
        if find_close_match:
            close_match = find_close_match[0]
            index_of_the_movie = df[df.title == close_match]['index'].values[0]
            similarity_score = list(enumerate(similarity[index_of_the_movie]))
            sorted_similar_movie = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:30]
            
            similar_movies = []
            for i, movie in enumerate(sorted_similar_movie, start=1):
                index = movie[0]
                title_from_index = df.loc[df.index == index, 'title'].values[0]
                similar_movies.append(f"{i}. {title_from_index}")
            
            return render(request, 'f_suggestion.html', {'similar_movies': similar_movies})
        else:
            return HttpResponse("No close match found for the provided movie name.")
    
    return render(request, 'f_suggestion.html')

def match_the_vibe(request):
    if request.method == 'POST':

        title = request.POST.get('title')

        genres = request.POST.getlist('genre') 
        genre = " ".join(genres)

        keyword = request.POST.get('keywords')
        keywords = keyword.lower()

        casts = request.POST.get('cast')
        cast = casts.title()

        directors = request.POST.get('director')
        director = directors.title()    
        
        csv_path = os.path.join(settings.STATIC_ROOT, 'movies.csv')
        df = pd.read_csv(csv_path)
        
        new_data = {'title': title, 'genres': genre, 'keywords': keywords, 'cast': cast, 'director': director}
        # Create a DataFrame
        # Create a dictionary with the data for the new row

        # Inserting the new row
        df.loc[len(df)] = new_data

        # Reset the index
        df = df.reset_index(drop=True)

        featured_columns = ['title', 'genres', 'keywords', 'cast', 'director']
        for fc in featured_columns:
            df[fc] = df[fc].fillna('')

        index_of_new_row = df.shape[0]-1

        combined_features = df['title'] + ' ' + df['genres'] + ' ' + df['keywords'] + ' ' + df['cast'] + ' ' + df['director']
        
        vectorizer = TfidfVectorizer()
        feature_vector = vectorizer.fit_transform(combined_features)
        similarity = cosine_similarity(feature_vector)

        
        similarity_score = list(enumerate(similarity[index_of_new_row]))
        sorted_similar_movie = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:30]
        
        similar_movies = []
        i=1
        for i, movie in enumerate(sorted_similar_movie, start=1):
                index = movie[0]
                title_from_index = df.loc[df.index == index, 'title'].values[0]
                similar_movies.append(f"{i}. {title_from_index}")            
            
        return render(request, 'match_the_vibe2.html', {'similar_movies': similar_movies})
    else:
        return render(request, 'match_the_vibe.html')
    
    
    
