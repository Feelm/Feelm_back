from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import RequestBoard, FreeBoard
from .serializers import *
from django.template.defaultfilters import linebreaks

# Create your views here.

@api_view(['GET','POST','PUT'])
def requests(request):
    if request.method == 'GET':
        requestboards = RequestBoard.objects.order_by('-id')
        serializer = RequestBoardSerializer(requestboards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RequestBoardCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({ 'message': '요청글 작성 완료' })
    elif request.method =='PUT':
        request_id = request.data['request_id']
        request_board=get_object_or_404(RequestBoard,pk= request_id)
        request_board.check=True
        request_board.save()
        return Response({'message': '확인완료'})

@api_view(['GET','POST'])
def free(request):
    if request.method == 'GET':
        FreeBoards = FreeBoard.objects.order_by('-id')
        serializer = FreeBoardSerializer(FreeBoards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(111111111111111111)
        serializer = FreeBoardCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            print(request.data)
            serializer.save(user=request.user)

            print(33333333333333333)
            return Response({ 'message': '자게 글 작성 완료' })

@api_view(['GET','PUT','DELETE'])
def free_detail(request, free_pk):
    if request.method == 'GET':
        freeboard = get_object_or_404(FreeBoard, pk= free_pk)
        freeboard.view_count+=1
        freeboard.content = linebreaks(freeboard.content)
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

@api_view(['POST'])
def free_like(request,free_pk):
    if request.method == 'POST':
        freeboard = get_object_or_404(FreeBoard, pk=free_pk)
        user = request.user
        if user != freeboard.user :
            if freeboard.like_users.filter(id=user.id).exists():
                freeboard.like_users.remove(user)
                result = f"{request.user}님이 {freeboard.user}님의 {free_pk}글의 좋아요를 취소합니다."
            else:
                freeboard.like_users.add(user)
                result = f"{request.user}님이 {freeboard.user}님의 {free_pk}글을 좋아합니다."
        else:
            result = "자신의 글은 좋아요 할 수 없습니다."
        return Response({
                "message": result
                })