from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    # 회원탈퇴
    path('withdraw/<int:user_pk>/', views.withdraw, name='withdraw'),

]