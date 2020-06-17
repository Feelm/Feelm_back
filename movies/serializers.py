from rest_framework import serializers
from .models import Movie, MovieStarPoint, Review, Comment, Genre
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserDetailSerializer

User = get_user_model()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fileds='__all__'

class MovieCreateSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(required=False)
    # overview=serializers.ModelSerializer(required=False)
    # backdrop_path = serializers.ModelSerializer(required=False)
    class Meta:
        model = Movie
        exclude = ['genres',]
        # fields = '__all__'

class MovieStarPointSerializer(serializers.ModelSerializer):
    # pointing_user = CustomUserDetailsSerializer(required=False)
    class Meta:
        model = MovieStarPoint
        fields = ( 'star_point','pointing_user', 'pointed_movie',)


class MovieListSerializer(serializers.ModelSerializer):
    # pointing_users = MovieStarPointSerializer(source='moviestarpoint_set', many=True, required=False)
    star = serializers.ReadOnlyField()
    class Meta:
        model = Movie
        fields = ('id', 'title','poster_path','vote_average' ,'pointing_users','star')
        # fields = '__all__'
        read_only_fields = ['pointing_users']


class MovieStarPointUpdateSerializer(serializers.ModelSerializer):
    # pointing_users = MovieStarPointSerializer(source='moviestarpoint_set', many=True, required=False)
    pointing_user = serializers.ModelSerializer(required=False)
    pointed_movie = serializers.ModelSerializer(required=False)
    # star_point = serializers.ModelSerializer()
    # print(star_point)
    class Meta:
        model = MovieStarPoint
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self,obj):
        return obj.user.name
    class Meta:
        model = Comment
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    like = serializers.ReadOnlyField()
    comments = CommentSerializer(source='comment_set' , many=True)
    
    def get_user(self,obj):
        return obj.user.name
    class Meta:
        model = Review
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    star = serializers.ReadOnlyField()
    reviews = ReviewDetailSerializer(source='review_set' , many=True)
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['pointing_users', 'reviews']


class ReviewCreateSerializer(serializers.ModelSerializer):
    movie = serializers.ModelSerializer(required=False)
    user = serializers.ModelSerializer(required=False)
    # like_user = serializers.ReadOnlyField(required=False)
    class Meta:
        model = Review
        fields = ['movie','user','title','content']
        # read_only_fields = ['like_user']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    like = serializers.ReadOnlyField()
    def get_user(self,obj):
        return obj.user.name
    class Meta:
        model = Review
        # fields = ['id', 'title', '']
        exclude = ['like_users']

class CommentCreateSerializer(serializers.ModelSerializer):
    review = serializers.ReadOnlyField(required = False)
    user = serializers.ReadOnlyField(required= False)

    class Meta:
        model = Comment
        fields = '__all__'






    
