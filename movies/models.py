from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
# Create your models here.
User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=30)

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
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
    pointing_users = models.ManyToManyField(User, related_name='pointed_movies', through='MovieStarPoint')
    nowplaying = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=False)
    
    @property
    def star(self):
        pointing_num = self.moviestarpoint_set.count()
        if pointing_num ==0:
            return self.vote_average
        else:
            return round(self.moviestarpoint_set.aggregate(Avg('star_point'))['star_point__avg'],1)



class MovieStarPoint(models.Model):
    star_point = models.FloatField(default=0, validators=[MinValueValidator(0),MaxValueValidator(10)])
    pointing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pointed_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')

    @property
    def like(self):
        number = self.like_users.count()
        return number


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
