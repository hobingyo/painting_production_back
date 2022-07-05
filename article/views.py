from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from django.utils import timezone
from ppb.permissions import IsAdminOrIsAuthenticatedReadOnly
from rest_framework.permissions import IsAuthenticated
from article.serializers import ArticleSerializer, ArticleImageSerializer, CommentSerializer, ArticlePostSerializer
import os
import shutil
import json
from rest_framework import permissions
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication
from user.jwt_claim_serializer import SpartaTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from PIL import Image
import io
from django.core.files.base import ContentFile




# Create your views here.


# url = 'article/'






class ArticleView(APIView): # CBV 방식
    # 로그인 한 사용자의 게시글 목록 return
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user
        today = timezone.now()

        articles = ArticleModel.objects.filter().order_by("-id")
        
        titles = []

        for article in articles:
            titles.append(article.title)
        
        return Response ({"article_list": titles})

    def post(self, request):


        user = request.user
        title = request.data.get('title','')
        contents = request.data.get('contents','')
        image = request.FILES['image']

        if len(title) <= 1 :
            return Response({"error":"title이 1자 이하라면 게시글을 작성할 수 없습니다."})
        if len(contents) <= 10 :
            return Response({"error":"contents가 10자 이하라면 게시글을 작성할 수 없습니다."}) 
        
        recent_article = ArticleModel.objects.latest('id')
        recent_article.image = image
        recent_article.title = title
        recent_article.contents = contents
        recent_article.save()


        # 유화작업 파트, 파일 크기 지정 --end-scale <>

        style_img = ArticleModel.objects.latest('id').image_converted
        text = f'{style_img}'
        if text[0] == 'p':
            output = os.system(f'style_transfer media/image/{image} media/{style_img} -o output_{image} --end-scale 50')
        else:
            output = os.system(f'style_transfer media/image/{image} {style_img} -o output_{image} --end-scale 50')
        
        output = f'output_{image}'
        shutil.move(f'{output}', f'media/output/{output}')

        empty_output = ArticleModel.objects.latest('id')
        empty_output.output = f'../output_{image}'
        empty_output.save()

        return Response({"message":"작성 완료!"})

    # 게시물 업데이트
    def put(self, request, obj_id):
    
    
        print(request.data)
        article = ArticleModel.objects.get(id=obj_id)
        article_serializer = ArticleSerializer(article, data=request.data, partial=True, context={"request": request})

        
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)

        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시물 삭제
    def delete(self, request, obj_id):
        
        obj = ArticleModel.objects.get(id=obj_id)
        title = obj.title 
        user = obj.author
        ArticleModel.objects.get(id=obj_id).delete()
        return Response({'message': f'{user}님의 {title}게시글이 삭제되었습니다.'})


# url = 'article/all/' 모든 아티클 리스팅
class AllArticleView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny]


    def get(self, request):

        articles = list(ArticleModel.objects.all().order_by("-id"))
        
        # for article in articles:
        result = ArticleSerializer(articles, many=True).data
        return Response(result) 

    # 적용 필터 가져오기
    def post(self, request):

        filter = request.data
        filter = f'media/paint/{filter}.png'
        ArticleModel.objects.create(
            image_converted=filter, 
            author=request.user, 
            title='', 
            contents='아직 작성되지 않았습니다.'
            )
        print(filter)
        return Response(filter)


# url = 'article/<obj_id>/ article detail 페이지
class ArticleDetailView(APIView):
    permisiion_classes = [IsAuthenticated]

    def get(self, request, obj_id):
        

        
        article_detail = ArticleModel.objects.get(id=obj_id)
        article_detail_username = article_detail.author.username
        
        return Response(ArticleSerializer(article_detail).data)

# 게시글 작성자 아이디로 불러오는 함수
class ArticleUserView(APIView):
    

    def get(self, request, obj_id):
        

        
        article_detail = ArticleModel.objects.get(id=obj_id)
        article_detail_username = article_detail.author.username
        
        return Response(article_detail_username)



class CommentView(APIView):
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    permission_classes = [permissions.AllowAny]

    def get(self, request, article_id):
        return Response(CommentSerializer(article_id).data)

    # 댓글 작성
    def post(self, request, article_id):
        
        
        user = request.user
        print(user)
        request.data['article'] = ArticleModel.objects.get(id=article_id)
        contents = request.data.get('contents','')

        comment = CommentModel(
            article = request.data['article'],
            user = user,
            contents = contents,
        )

        comment.save()
        return Response({"message":"댓글 작성 완료!"})

    # 댓글 업데이트
    def put(self, request, comment_id):
        data = request.data
        comment = CommentModel.objects.get(id=comment_id)
        comment_serializer = CommentSerializer(comment, data, partial=True, context={"request": request})

        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    def delete(self, request, comment_id):
        
        obj = CommentModel.objects.get(id=comment_id)
        user = obj.user
        author = obj.article.author
        CommentModel.objects.get(id=comment_id).delete()

        if request.user == user:
            return Response({'message': f'{user}님의 댓글이 삭제되었습니다.'})
        
        elif request.user == author:
            return Response({'message': f'{user}님의 댓글이 삭제되었습니다.'})
        
        else:
            return Response({'error': '댓글 삭제 권한이 없습니다'})
    


# 코멘트 작성자 아이디로 불러오는 함수
class CommentUserView(APIView):
    

    def get(self, request, comment_id):
        

        
        comment_detail = CommentModel.objects.get(id=comment_id)
        comment_detail_user = comment_detail.user.username
        
        return Response(comment_detail_user)



class ImageView(APIView):
    


    # 그림판 필터 가져와서 저장하기 
    def post(self,request):
        print(request.user)
        
        data = request.data
        data = data['image']
        
        
        ArticleModel.objects.create(
            image_converted=data, 
            author=request.user, 
            title='', 
            contents='아직 작성되지 않았습니다.'
            )
        print(data)
        return Response("")

class UserImageView(APIView):

    # 드래그앤 드롭 파일(적용파일)가져와서 저장하기 
    def post(self,request):
        data = request.data
        data1 = request.FILES
        print(data1.values())
        print(dir(data1))
        recent_article = ArticleModel.objects.latest('id')

        recent_article.image = data
        recent_article.save()

        return Response("")
