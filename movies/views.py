from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie, Movie_Star_Point
from .serializers import MovieListSerializer

# 라인브레이크
# from django.template.defaultfilters import linebreaks

# Create your views here.
@api_view(['GET'])
def index(request):
    movies = Movie.objects.order_by('-release_date')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)
