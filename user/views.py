from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status


from django.contrib.auth import login, logout, authenticate
from user.serializers import UserSerializer, UserProfileSerializer, UserListingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.jwt_claim_serializer import SpartaTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from user.models import UserProfile, User


class UserView(APIView):  # CBV 방식
    permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능

    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능


    # # 유저 정보 보기
    # def get(self, request):
    #     user = request.user
    #     return Response(UserSerializer(user).data)

    
    def get(self, request):
        user = list(User.objects.all())
        return Response(UserListingSerializer(user, many=True).data)




    # 회원가입
    def post(self, request):
        password = request.data.pop("password")
        user = User(**request.data)
        user.set_password(password)
        user.save()
        return Response({"message": "회원가입 성공!!"}, status=status.HTTP_200_OK)
        

    def put(self, request):
        return Response({'message': 'put method!!'})


    def delete(self, request):
        return Response({'message': 'delete method!!'})



class UserApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK, )



    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!!"}, status=status.HTTP_200_OK)



# jwt_claim_serializer.py에서 커스터마이징 한 방식을 적용
class SpartaTokenObtainPairView(TokenObtainPairView):
    # serializer_class 변수에 커스터마이징 된 시리얼라이저를 넣어 준다.
    serializer_class = SpartaTokenObtainPairSerializer



# 인가된 사용자만 접근할 수 있는 View 생성
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
		# JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
				# Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})



# 마이페이지 리스팅관련 시리얼라이저 view 생성
class UserProfileApiview(APIView):


    # JWT token으로 인가된 사용자만 접근할 수 있게
    permission_classes = [permissions.IsAuthenticated]

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)