from django.contrib import admin
from .models import Movie, Genre, Movie_Star_Point
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Movie_Star_Point)