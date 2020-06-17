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
            serializers = MovieCreateSerializer(data=res)

            if not res['release_date']=='':
                release_date= datetime.strptime(res['release_date'],"%Y-%m-%d")
                if datetime.today()>release_date:
                    upcoming = False
                else:
                    upcoming = True
                if 0<=(datetime.today()-release_date).days <30:
                    nowplaying = True
                else:
                    nowplaying = False
            else:
                upcoming = False
                nowplaying = False
                res['release_date'] = datetime.utcfromtimestamp(0).date()
            if not res['overview'] : 
                res['overview'] = "제공하지않음"
            if not res['backdrop_path']:
                res['backdrop_path']="/"
            if not res['poster_path']:
                res['poster_path']='/'
            if serializers.is_valid(raise_exception=True):
                serializers.save(release_date=res['release_date'],genres= [i['id'] for i in res['genres']], upcoming=upcoming, nowplaying=nowplaying, overview=res['overview'], backdrop_path=res['backdrop_path'],poster_path=res['poster_path'])
            result = '영화가 추가 되었습니다.'
        else:
            result = '이미 있는 영화입니다.'
        return Response({'message': result})
        

@api_view(['POST','PUT'])
def point(request,movie_pk):
    if request.method == 'POST':
        print(request.GET,request.POST, request.data)
        serializer = MovieStarPointUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
    movies = Movie.objects.filter(upcoming=True).order_by('-release_date')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recent(request):
    movies = Movie.objects.filter(upcoming=False).order_by('-release_date')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def latest(request):
    movies = Movie.objects.filter(adult=False).order_by('-release_date')[:10]
    ran_movie = random.randrange(0,10)
    serializer = MovieDetailSerializer(movies[ran_movie])
    return Response(serializer.data)


@api_view(['GET'])
def recommend(request):
    if not request.user.is_authenticated or request.user.pointed_movies.count()==0:
        print(999999999999)
        movies = Movie.objects.filter(upcoming=False).order_by('-release_date')[:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data) 
    elif request.user.pointed_movies.count()>0:
        print('로그인상태')
        recommend_list =[]
        recommend_id_list=[]
        most_movie = request.user.moviestarpoint_set.order_by('-star_point')[:5]
        for i in most_movie:
            url = f'https://api.themoviedb.org/3/movie/{i.pointed_movie.id}/recommendations?api_key=fcf50b1b6b84aa2265ae58bcd7596305&language=ko-KR&page=1'
            res = requests.get(url).json()['results'][:2]
            for j in res:
                if j['id'] not in recommend_id_list:
                    recommend_id_list.append(j['id'])
        cnt=0
        while len(recommend_id_list)<10:
            url = f'https://api.themoviedb.org/3/movie/{most_movie[0].pointed_movie.id}/recommendations?api_key=fcf50b1b6b84aa2265ae58bcd7596305&language=ko-KR&page=1'
            res = requests.get(url).json()['results'][cnt+2]
            if res['id'] not in recommend_id_list:
                recommend_id_list.append(res['id'])
                cnt+=1

        # 추천영화가 db에 없으면 db에 추가
        for i in recommend_id_list:
            temp_id = i
            if not Movie.objects.filter(id=temp_id).exists():
                print(temp_id)
                url = f'https://api.themoviedb.org/3/movie/{temp_id}?api_key=fcf50b1b6b84aa2265ae58bcd7596305&language=ko-KR'
                res = requests.get(url).json()
                serializers = MovieCreateSerializer(data=res)
                if not res['release_date']=='':
                    release_date= datetime.strptime(res['release_date'],"%Y-%m-%d")
                    if datetime.today()>release_date:
                        upcoming = False
                    else:
                        upcoming = True
                    if 0<=(datetime.today()-release_date).days <30:
                        nowplaying = True
                    else:
                        nowplaying = False
                else:
                    upcoming = False
                    nowplaying = False
                    res['release_date'] = datetime.utcfromtimestamp(0).date()
                if not res['overview'] : 
                    res['overview'] = "제공하지않음"
                if not res['backdrop_path']:
                    res['backdrop_path']="/"
                if not res['poster_path']:
                    res['poster_path']='/'
                if serializers.is_valid(raise_exception=True):
                    serializers.save(release_date=res['release_date'],genres= [i['id'] for i in res['genres']], upcoming=upcoming, nowplaying=nowplaying, overview=res['overview'], backdrop_path=res['backdrop_path'],poster_path=res['poster_path'])
        print('2342903rufj9023jf0')
        for reco_id in recommend_id_list:
            movie = get_object_or_404(Movie, pk=reco_id)
            recommend_list.append(movie)
        serializer = MovieListSerializer(recommend_list, many=True)
        return Response(serializer.data)


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

