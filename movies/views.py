from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg, Max, Min, Sum, Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie, MovieStarPoint, Review
from .serializers import * #MovieDetailSerializer,MovieListSerializer, MovieStarPointSerializer, MovieStarPointUpdateSerializer, ReviewCreateSerializer, ReviewDetailSerializer
# from boards.serializers import RequestBoardSerializer
import random 
import requests
from datetime import datetime
# 라인브레이크
# from django.template.defaultfilters import linebreaks


User = get_user_model()
# Create your views here.
@api_view(['GET'])
def index(request):
    movies = Movie.objects.order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
def movie_detail(request,movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not Movie.objects.filter(id=movie_pk).exists():
            url = f'https://api.themoviedb.org/3/movie/{movie_pk}?api_key=fcf50b1b6b84aa2265ae58bcd7596305&language=ko-KR'
            res = requests.get(url).json()
            movie = Movie()
            movie.id = res['id']
            movie.title = res['title']
            movie.original_title = res['original_title']
            movie.release_date = res['release_date']
            movie.popularity = res['popularity']
            movie.vote_count = res['vote_count']
            movie.vote_average = res['vote_average']
            movie.adult = res['adult']
            movie.overview = res['overview']
            movie.original_language = res['original_language']
            movie.poster_path = res['poster_path']
            movie.backdrop_path = res['backdrop_path']
            movie.genres_set = res['genres']
            if datetime.today().strftime("%Y-%m-%d")>res['release_date']:
                movie.upcoming = False
            else:
                movie.upcoming = True
            movie.nowplaying = False
            movie.save()
  
            result = '영화가 추가 되었습니다.'
        else:
            result = '이미 있는 영화입니다.'
        return Response({'message': result})
        


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


@api_view(['GET','POST'])
def review(request,movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        reviews = movie.review_set.order_by('-id')
        serializers = ReviewSerializer(reviews, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':    
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            movie = get_object_or_404(Movie,pk=movie_pk)
            # # 테스트용
            # user = get_object_or_404(User,pk=1)
            # serializer.save(user=user,movie=movie)
            # 실제 유저용
            serializer.save(user=request.user,movie=movie)
            result ="성공적으로 리뷰가 작성되었습니다."
        return Response({
            "message":result,
            })

@api_view(['GET','PUT','DELETE'])
def review_detail(request,movie_pk,review_pk):
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
        if request.user == review.user:
            review.delete()
            result = f"{review_pk}글이 성공적으로 삭제되었습니다."
        else:
            result = '다른사람의 글은 삭제 할 수 없습니다.'
        return Response({
                "message": result,
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

@api_view(['GET','POST'])
def comment(request, movie_pk, review_pk):
    if request.method == 'GET':
        review = get_object_or_404(Review, pk = review_pk)
        comments = review.comment_set.order_by('-id')
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            review = get_object_or_404(Review,pk=review_pk)
            # # 테스트용
            # user = get_object_or_404(User,pk=1)
            # serializer.save(user=user,movie=movie)
            # 실제 유저용
            serializer.save(user=request.user,review=review)
            return Response({
                "message":"성공적으로 댓글이 작성되었습니다.",
                })

@api_view(['DELETE'])
def comment_detail(request,movie_pk,review_pk,comment_pk):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = request.user
        if request.user == comment.user:
            comment.delete()
            result = f"{comment_pk}글이 성공적으로 삭제되었습니다."
        else:
            result = '다른사람의 글은 삭제 할 수 없습니다.'
        return Response({
                "message": result,
                })

