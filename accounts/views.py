from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_auth.models import TokenModel
# Create your views here.

print(TokenModel.objects.all())
User=get_user_model()
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


