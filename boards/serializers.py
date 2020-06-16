from rest_framework import serializers
from .models import RequestBoard

class RequestBoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.ModelSerializer(required = False)
    class Meta:
        model = RequestBoard
        # fields= '__all__'
        fields = ['movie_id', 'movie_name', 'title','user']

class RequestBoardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self,obj):
        return obj.user.name
    class Meta:
        model = RequestBoard
        fields = '__all__'