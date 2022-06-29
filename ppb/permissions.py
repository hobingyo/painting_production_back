from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils import timezone
from argon2 import PasswordHasher
from rest_framework.exceptions import APIException
from rest_framework import permissions,status

class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class RegistedUser(BasePermission):
    """
    가입일 기준 3일 이상 지난 사용자만 접근 가능
    """
    SAFE_METHODS = ('GET', )
    message = '가입 후 5초 이상 지난 사용자만 글을 작성하실 수 있습니다.'
    
    def has_permission(self, request, view):

        if bool(request.user and request.user.join_date < (timezone.now() - timedelta(seconds=5))) is True:
            return True

        elif request.method in self.SAFE_METHODS:
            return True
        
        else:
            return False

class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

        if user.is_authenticated and user.is_admin or user.join_date < (timezone.now() - timedelta(days=7)):
            
            return True

        return False