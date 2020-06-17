from django.contrib import admin
from .models import Movie, Genre, MovieStarPoint, Review, Comment
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieStarPoint)
admin.site.register(Review)
admin.site.register(Comment)
