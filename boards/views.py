from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import RequestBoard, FreeBoard
from .serializers import *
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

@api_view(['GET','POST'])
def free(request):
    if request.method == 'GET':
        FreeBoards = FreeBoard.objects.all()
        serializer = FreeBoardSerializer(FreeBoards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FreeBoardCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({ 'message': '자게 글 작성 완료' })

@api_view(['GET','PUT','DELETE'])
def free_detail(request, free_pk):
    if request.method == 'GET':
        freeboard = get_object_or_404(FreeBoard, pk= free_pk)
        freeboard.view_count+=1
        freeboard.save()
        serializer = FreeBoardSerializer(freeboard)
        return Response(serializer.data)
    elif request.method == 'PUT':
        freeboard = get_object_or_404(FreeBoard, pk= free_pk)
        serializer = FreeBoardCreateSerializer(freeboard, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": f"{free_pk}글이 성공적으로 수정되었습니다.",
                })
    elif request.method == 'DELETE':
        freeboard = get_object_or_404(FreeBoard, pk=free_pk)
        if request.user == freeboard.user:
            freeboard.delete()
            result = f"{free_pk}글이 성공적으로 삭제되었습니다."
        else:
            result = '다른사람의 글은 삭제 할 수 없습니다.'
        return Response({
                "message": result,
                })