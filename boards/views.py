from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import RequestBoard
from .serializers import RequestBoardSerializer, RequestBoardCreateSerializer
# Create your views here.

@api_view(['GET','POST'])
def requests(request):
    if request.method == 'GET':
        requestboards = RequestBoard.objects.all()
        serializer = RequestBoardSerializer(requestboards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RequestBoardCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({ 'message': '요청 완료' })