from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Movie, MovieStarPoint
from .serializers import MovieListSerializer, MovieStarPointSerializer, MovieStarPointUpdateSerializer

# 라인브레이크
# from django.template.defaultfilters import linebreaks

# Create your views here.
@api_view(['GET'])
def index(request):
    movies = Movie.objects.order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
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
                "message":"성공적으로 생성되었습니다.",})
    elif request.method == 'PUT':
        point = MovieStarPoint.objects.filter(pointed_movie=movie_pk).filter(pointing_user=request.user.pk)
        print(point)
        serializer = MovieStarPointUpdateSerializer(point[0],data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"성공적으로 수정되었습니다.",})


