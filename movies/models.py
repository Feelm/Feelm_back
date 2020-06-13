from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=30)

class Movie(models.Model):
    title = models.CharField(max_length=300)
    original_title = models.CharField(max_length=300)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=10)
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100, default='')
    genres = models.ManyToManyField(Genre, related_name='movies')
    pointing_users = models.ManyToManyField(User, related_name='pointed_movies', through='Movie_Star_Point')


class Movie_Star_Point(models.Model):
    pointing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pointed_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    star_point = models.IntegerField(default=0)

    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')