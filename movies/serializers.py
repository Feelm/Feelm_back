from rest_framework import serializers
from .models import Movie, Movie_Star_Point
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserDetailsSerializer

User = get_user_model()
# class ArticleListSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()

#     class Meta:
#         model = Article
#         fields = ('id', 'title', 'user',)

class MovieStarPointSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    class Meta:
        model = Movie_Star_Point
        fields = ('user', 'movie', 'star_point')


class MovieListSerializer(serializers.ModelSerializer):
    pointing_users = MovieStarPointSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'pointing_users',)

