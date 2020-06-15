from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 영화 최신순으로 모든 리스트 GET
    path('', views.index, name='index'),
    # 영화 하나하나 디테일 GET 관리자만 영화 추가가능 POST
    path('<int:movie_pk>/', views.movie_detail, name = 'movie_detail'),
    # 영화 하나의 별점 부여 (POST), 별점 수정(PUT)
    path('<int:movie_pk>/point/', views.point, name = 'point'),
    # 현재상영작 리스트 GET
    path('nowplaying/', views.nowplaying, name ='nowplaying'),
    # 상영예정작 GET
    path('upcoming/', views.upcoming, name ='upcoming'),
    # 최신작 GET
    path('recent/', views.recent, name ='recent'),
    # 추천작 GET
    path('recommend/', views.recommend, name = 'recommend'),
    # 가장 최신작 랜덤 1개
    path('latest/', views.latest, name='latest'),
    # 리뷰 리스트 GET,생성 POST
    path('<int:movie_pk>/reviews/', views.review, name='review'),
    # 리뷰 하나 세부 작업 | 리뷰 상세 GET , 리뷰 수정 PUT , 리뷰 삭제 DELETE
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail, name='review_detail'),
    # 리뷰 좋아요 POST
    path('<int:movie_pk>/reviews/<int:review_pk>/like/', views.review_like, name='review_like'),
    # 리뷰에 달린 댓글 리스트 GET, 댓글 작성 POST
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/', views.comment, name='comment'),
    # 댓글 삭제 DELETE
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
]