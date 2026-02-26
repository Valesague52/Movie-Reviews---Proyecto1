from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images/', blank=True, null=True)
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)  # ← NUEVO
    year = models.IntegerField(blank=True, null=True)  # ← NUEVO
    
    def __str__(self):
        return self.title