from django.shortcuts import render
from .models import Movie  # ← Esta línea es importante

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

import matplotlib.pyplot as plt
import matplotlib
import io
import base64
from django.db.models import Count
from django.shortcuts import render

def statistics_view(request):
    matplotlib.use('Agg')
    
    from .models import Movie
    
    # Gráfica por año
    years = Movie.objects.values('year').annotate(count=Count('year')).order_by('year')
    year_counts = {}
    for item in years:
        year = item['year'] if item['year'] else 'Sin año'
        year_counts[year] = item['count']
    
    # Crear gráfica de años
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(year_counts)), list(year_counts.values()), color='skyblue')
    plt.title('Películas por Año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad')
    plt.xticks(range(len(year_counts)), list(year_counts.keys()), rotation=45)
    plt.tight_layout()
    
    # Guardar gráfica de años
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    graphic_year = base64.b64encode(buffer_year.getvalue()).decode('utf-8')
    
    # Gráfica por género
    all_movies = Movie.objects.all()
    genre_counts = {}
    
    for movie in all_movies:
        if movie.genre:
            # Tomar el primer género si hay varios
            if '|' in movie.genre:
                first_genre = movie.genre.split('|')[0].strip()
            else:
                first_genre = movie.genre.strip()
            
            genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1
    
    # Crear gráfica de géneros
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(genre_counts)), list(genre_counts.values()), color='lightcoral')
    plt.title('Películas por Género')
    plt.xlabel('Género')
    plt.ylabel('Cantidad')
    plt.xticks(range(len(genre_counts)), list(genre_counts.keys()), rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar gráfica de géneros
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    graphic_genre = base64.b64encode(buffer_genre.getvalue()).decode('utf-8')
    
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })
    
def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})