from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_auth.models import TokenModel
from rest_framework.decorators import api_view, permission_classes
# Create your views here.

User=get_user_model()
@api_view(['GET'])
def withdraw(request, user_pk):
    user= get_object_or_404(User,pk=user_pk)
    if request.user == user:
        name= user.name
        token = get_object_or_404(TokenModel, user_id=1)
        token.delete()
        user.delete()
        result= f'{name}님의 계정이 삭제되었습니다.'
    else:
        result = '본인만 탈퇴가 가능합니다.'
    return Response({ 'message' : result })


