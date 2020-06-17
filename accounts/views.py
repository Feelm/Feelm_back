from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_auth.models import TokenModel
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

User=get_user_model()



@api_view(['GET'])
def withdraw(request, user_pk):
    print(0)
    user = get_object_or_404(User,pk=user_pk)
    print(user)
    if request.user == user:
        name= user.name
        print(1)
        token = get_object_or_404(TokenModel, user_id=user_pk)
        print(2)
        token.delete()
        print(3)
        user.delete()
        print(4)
        result= f'{name}님의 계정이 삭제되었습니다.'
    else:
        result = '본인만 탈퇴가 가능합니다.'
    return Response({ 'message' : result })


