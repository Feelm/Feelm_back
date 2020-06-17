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



class FreeBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name='like_freeboards')

    @property
    def like(self):
        number = self.like_users.count()
        print(number)
        return number