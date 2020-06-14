from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg, Max, Min, Sum, Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie, MovieStarPoint, Review
from .serializers import MovieDetailSerializer,MovieListSerializer, MovieStarPointSerializer, MovieStarPointUpdateSerializer, ReviewCreateSerializer, ReviewDetailSerializer

import random 

# 라인브레이크
# from django.template.defaultfilters import linebreaks


User = get_user_model()
# Create your views here.
@api_view(['GET'])
def index(request):
    movies = Movie.objects.order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)


@api_view(['POST','PUT'])
def point(request,movie_pk):
    if request.method == 'POST':
        serializer = MovieStarPointUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
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

@api_view(['GET'])
def latest(request):
    movies = Movie.objects.order_by('-release_date')[:10]
    ran_movie = random.randrange(0,10)
    serializer = MovieDetailSerializer(movies[ran_movie])
    return Response(serializer.data)


@api_view(['GET'])
def recommend(request):
    User=get_user_model()
    admin = get_object_or_404(User,pk = 1)
    print(admin.pointed_movies.pointed_movie)

    # movies = Movie.objects.filter(upcoming=False).order_by('-release_date')[:10]
    # serializer = MovieListSerializer(movies, many=True)
    # return Response(serializer.data)
    return


@api_view(['POST'])
def review_create(request,movie_pk):
    serializer = ReviewCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        movie = get_object_or_404(Movie,pk=movie_pk)
        # 테스트용
        user = get_object_or_404(User,pk=1)
        serializer.save(user=user,movie=movie)
        # # 실제 유저용
        # serializer.save(user=request.user,movie=movie)
        return Response({
            "message":"성공적으로 글이 작성되었습니다.",
            })

@api_view(['GET','PUT','DELETE'])
def review(request,movie_pk,review_pk):
    if request.method == 'GET':
        review = get_object_or_404(Review, pk= review_pk)
        review.view_count+=1
        review.save()
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        review = get_object_or_404(Review, pk= review_pk)
        serializer = ReviewCreateSerializer(review, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": f"{review_pk}글이 성공적으로 수정되었습니다.",
                })
    elif request.method == 'DELETE':
        review = get_object_or_404(Review, pk=review_pk)
        review.delete()
        return Response({
                "message": f"{review_pk}글이 성공적으로 삭제되었습니다.",
                })

@api_view(['POST'])
def review_like(request,movie_pk,review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
        if user != review.user :
            if review.like_users.filter(id=user.id).exists():
                review.like_users.remove(user)
                result = f"{request.user}님이 {review.user}님의 {review_pk}글의 좋아요를 취소합니다."
            else:
                review.like_users.add(user)
                result = f"{request.user}님이 {review.user}님의 {review_pk}글을 좋아합니다."
        else:
            result = "자신의 글은 좋아요 할 수 없습니다."
        return Response({
                "message": result
                })
