from django.urls import path
from . import views
app_name = 'boards'

urlpatterns = [
    path('requests/', views.requests, name='requests'),
    
]