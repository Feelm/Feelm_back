from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
# 유저가 영화검색-올려주세요-

User = get_user_model()
class RequestBoard(models.Model):
    movie_id = models.IntegerField()
    movie_name = models.CharField(max_length=300)
    title = models.CharField(max_length = 500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check = models.BooleanField(default=False)



