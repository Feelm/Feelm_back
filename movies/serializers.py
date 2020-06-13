from rest_framework import serializers
from .models import Movie, Movie_Star_Point
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserDetailsSerializer

User = get_user_model()

class MovieStarPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_Star_Point
        fields = ('pointing_user', 'pointed_movie', 'star_point')
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
    # pointing_users = MovieStarPointSerializer(many=True, required=False)

    class Meta:
        model = Movie
        # fields = ('id', 'title',)
        fields = '__all__'
        read_only_fields = ['pointing_users']

