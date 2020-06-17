from django.urls import path
from . import views
app_name = 'boards'

urlpatterns = [
    path('requests/', views.requests, name='requests'),
    path('free/' , views.free, name='free'),
    path('free/<int:free_pk>/', views.free_detail, name='free_detail'),
    path('free/<int:free_pk>/like/', views.free_like, name='free_like'),
    
]