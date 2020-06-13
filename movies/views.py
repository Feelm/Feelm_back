from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Movie, MovieStarPoint
from .serializers import MovieDetailSerializer,MovieListSerializer, MovieStarPointSerializer, MovieStarPointUpdateSerializer

from django.db.models import Avg, Max, Min, Sum, Count

# 라인브레이크
# from django.template.defaultfilters import linebreaks

# Create your views here.
@api_view(['GET'])
def index(request):
    movies = Movie.objects.order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # print(movie.star)
    # point = MovieStarPoint.objects.filter(pointed_movie=movie_pk).aggregate(Avg('star_point'))['star_point__avg']
    serializer = MovieDetailSerializer(movie)
    # print(serializer.data.star)
    return Response(serializer.data)


@api_view(['POST','PUT'])
def point(request,movie_pk):
    if request.method == 'POST':
        serializer = MovieStarPointUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # User = get_user_model()
            # user= get_object_or_404(User, pk=1)
            movie = get_object_or_404(Movie,pk=movie_pk)
            serializer.save(pointing_user=request.user,pointed_movie=movie)
            return Response({
                "message":"성공적으로 생성되었습니다.",
                })
    elif request.method == 'PUT':
        point = MovieStarPoint.objects.filter(pointed_movie=movie_pk).filter(pointing_user=request.user.pk)
        serializer = MovieStarPointUpdateSerializer(point[0],data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"성공적으로 수정되었습니다.",
                })

@api_view(['GET'])
def nowplaying(request):
    movies = Movie.objects.filter(nowplaying=True).order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def upcoming(request):
    movies = Movie.objects.filter(upcoming=True).order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recent(request):
    movies = Movie.objects.filter(upcoming=False).order_by('-release_date')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)
