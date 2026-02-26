from django.shortcuts import render
from .models import Movie
from django.db.models import Count
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
import re
from collections import Counter

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    total_peliculas = Movie.objects.count()
    return render(request, 'about.html', {'total_peliculas': total_peliculas})

def statistics_view(request):
    matplotlib.use('Agg')
    
    # Gráfica por año
    years = Movie.objects.values('year').annotate(count=Count('year')).order_by('year')
    year_counts = {}
    for item in years:
        year = item['year'] if item['year'] else 'Sin año'
        year_counts[year] = item['count']
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(year_counts)), list(year_counts.values()), color='skyblue')
    plt.title('Películas por Año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad')
    plt.xticks(range(len(year_counts)), list(year_counts.keys()), rotation=45)
    plt.tight_layout()
    
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    graphic_year = base64.b64encode(buffer_year.getvalue()).decode('utf-8')
    
    # Gráfica por género
    all_movies = Movie.objects.all()
    genre_counter = Counter()
    
    for movie in all_movies:
        if movie.genre:
            genres = re.split(r'[|,]', movie.genre)
            for g in genres:
                genre = g.strip().lower().capitalize()
                if genre and genre not in ['', 'none', 'n/a']:
                    genre_counter[genre] += 1
    
    top_genres = dict(genre_counter.most_common(15))
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_genres)), list(top_genres.values()), color='lightcoral')
    plt.title('Películas por Género (Top 15)')
    plt.xlabel('Género')
    plt.ylabel('Cantidad de películas')
    plt.xticks(range(len(top_genres)), list(top_genres.keys()), rotation=45, ha='right')
    plt.tight_layout()
    
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    plt.close()
    graphic_genre = base64.b64encode(buffer_genre.getvalue()).decode('utf-8')
    
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})