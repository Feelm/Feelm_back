from rest_framework import serializers
from .models import Movie, MovieStarPoint
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserDetailsSerializer

User = get_user_model()

class MovieStarPointSerializer(serializers.ModelSerializer):
    # pointing_user = CustomUserDetailsSerializer(required=False)
    class Meta:
        model = MovieStarPoint
        fields = ( 'star_point','pointing_user', 'pointed_movie',)


class MovieListSerializer(serializers.ModelSerializer):
    pointing_users = MovieStarPointSerializer(source='moviestarpoint_set', many=True, required=False)
    class Meta:
        model = Movie
        fields = ('id', 'title','pointing_users')
        # fields = '__all__'
        read_only_fields = ['pointing_users']

class MovieStarPointUpdateSerializer(serializers.ModelSerializer):
    # pointing_users = MovieStarPointSerializer(source='moviestarpoint_set', many=True, required=False)
    pointing_user = serializers.ModelSerializer(required=False)
    pointed_movie = serializers.ModelSerializer(required=False)
    class Meta:
        model = MovieStarPoint
        fields = '__all__'

