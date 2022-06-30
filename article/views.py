from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from django.utils import timezone
from ppb.permissions import IsAdminOrIsAuthenticatedReadOnly
from rest_framework.permissions import IsAuthenticated
from article.serializers import ArticleSerializer, ArticleImageSerializer, CommentSerializer
import os
# Create your views here.


# url = 'article/'
class ArticleView(APIView): # CBV 방식
    # 로그인 한 사용자의 게시글 목록 return
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user
        today = timezone.now()

        articles = ArticleModel.objects.filter(
            exposure_start_date__lte = today
        ).order_by("-id")
        
        titles = []

        for article in articles:
            titles.append(article.title)
        
        return Response ({"article_list": titles})

    def post(self, request):
        user = request.user
        title = request.data.get('title','')
        contents = request.data.get('contents','')
        image = request.FILES['image'].name
        # exposure_start_date = request.data.get('exposure_start_date')
        # exposure_end_date = request.data.get('exposure_start_date')

        if len(title) <= 1 :
            return Response({"error":"title이 1자 이하라면 게시글을 작성할 수 없습니다."})
        if len(contents) <= 10 :
            return Response({"error":"contents가 10자 이하라면 게시글을 작성할 수 없습니다."}) 
            


        article = ArticleModel(
            author = user,
            title = title,
            contents = contents,
            image = request.FILES['image'],
            # exposure_start_date = exposure_start_date,
            # exposure_end_date = exposure_end_date
        )

        article.save()

        # style transfer 부분
        # 실험파일
        output = request.FILES['image']

        # 머신러닝 파트
        # output = os.system(f'style_transfer article/media/{image} article/media/boo.png -o output_{image}')

        empty_output = ArticleModel.objects.latest('id')

        # 아웃풋 삽입
        empty_output.output = output

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


# url = 'article/allarticle/' 모든 아티클 리스팅
class AllArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now()

        articles = ArticleModel.objects.filter(
                exposure_start_date__lte = today
            ).order_by("-id")
        
        articles = ArticleModel.objects.all()
        for article in articles:
            
            return Response(ArticleImageSerializer(article).data) 


# url = 'article/<obj_id>/ article detail 페이지
class ArticleDetailView(APIView):
    permisiion_classes = [IsAuthenticated]

    def get(self, request, obj_id):
        
        article_detail = ArticleModel.objects.get(id=obj_id)
        return Response(ArticleSerializer(article_detail).data)




class CommentView(APIView):
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request, article_id):
        return Response(CommentSerializer(article_id).data)

    # 댓글 작성
    def post(self, request, article_id):
        
        user = request.user
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
        
        comment = CommentModel.objects.get(id=comment_id)
        comment_serializer = CommentSerializer(comment, data=request.data, partial=True, context={"request": request})

        
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
    






















# class ArticleDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         today = timezone.now()

#         articles_comment = CommentModel.objects.comment(
#                 exposure_start_date__lte = today
#             ).order_by("-id")

#         comments = []

#         for comment in articles_comment:
#             comments.append(comment.comment)
#             return Response ({"comment_list": comments}) 