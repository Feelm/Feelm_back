from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/point/', views.point, name='point'),
    path('nowplaying/', views.nowplaying, name='nowplaying'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('recent/', views.recent, name='recent'),
    
    # path('create/', views.movie_create, name='movie_create'),
    # path('<int:movie_pk>/update/', views.movie_update, name='movie_update'),
    # path('<int:movie_pk>/delete/', views.movie_delete, name='movie_delete'),
    # path('<int:movie_pk>/detail/', views.movie_detail, name='movie_detail'),
    # path('<int:movie_pk>/reviews/', views.review_create, name='review_create'),
    # path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail, name='review_detail'),
    # path('<int:movie_pk>/reviews/<int:review_pk>/update/', views.review_update, name='review_update'),
    # path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    # path('<int:movie_pk>/reviews/<int:review_pk>/like/', views.review_like, name='like'),
    # path('<int:movie_pk>/reviews/<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    # path('<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]