from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images/', blank=True, null=True)  # ← Añade blank=True y null=True
    url = models.URLField(blank=True)
    
    def __str__(self):
        return self.title