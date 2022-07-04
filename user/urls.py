from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserView, 
    UserApiView, 
    SpartaTokenObtainPairView, 
    OnlyAuthenticatedUserView
)
from user import views

urlpatterns = [
    # user/
    path('', UserView.as_view()),
    path('mypage/', views.UserProfileApiview.as_view()),
    path('login/', UserApiView.as_view()),
    path('logout/', UserApiView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sparta/token/', SpartaTokenObtainPairView.as_view(), name='sparta_token'),
    path('api/authonly/', OnlyAuthenticatedUserView.as_view()),
]