from rest_framework import serializers
from .models import Movie, MovieStarPoint
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserDetailsSerializer

User = get_user_model()

class MovieStarPointSerializer(serializers.ModelSerializer):
    # pointing_user = serializers.ReadOnlyField(source='pointing_users.user')
    # pointed_movie = serializers.ReadOnlyField(source='movie.id')
    
    class Meta:
        model = MovieStarPoint
        fields = ( 'star_point','pointing_user', 'pointed_movie',)
        # fields= '__all__'

# class MovieSerializer(serializers.ModelSerializer):
#     pointing_users = serializers.SerializerMethodField()
#     class Meta:
#         model = Movie
#         fields = ('id','title', 'pointing_users' )

#     def get_pointing_users(self,obj):
#         qset = Movie_Star_Point.objects.filter(movie=obj)
#         return [MovieStarPointSerializer(m).data for m in qset]




class MovieListSerializer(serializers.ModelSerializer):
    pointing_users = MovieStarPointSerializer(source='moviestarpoint_set', many=True, required=False)
    # pointing_users = MovieStarPointSerializer(source='pointed_movie_set',many=True, read_only=True, required=False)
    class Meta:
        model = Movie
        # fields = ('id', 'title',)
        fields = '__all__'
        read_only_fields = ['pointing_users']

