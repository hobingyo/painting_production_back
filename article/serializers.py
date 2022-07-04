from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from user.models import User as User


class CommentSerializer(serializers.ModelSerializer):
    comments_article = serializers.SerializerMethodField()

    def get_comments_article(self,obj):
        return obj.article.id

    



    # custom validation
    def validate(self, request, data):
        
        if self.context['request'].method == 'PUT' or 'DELETE':
            request.user
            return data




    # custum update
    def update(self, instance, validated_data):

        # instance에는 입력된 object가 담긴다.
        print(validated_data)
        for key, value in validated_data.items():
            if key == "user":
                instance.user(value)
                continue

            setattr(instance, key, value)
        instance.save()
        return instance

    
    class Meta :
        model = CommentModel
        fields = ['id', 'article', 'user', 'contents', 'comments_article']


class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)


    # custum update
    def update(self, instance, validated_data):

        # instance에는 입력된 object가 담긴다.
        print(validated_data)
        for key, value in validated_data.items():
            if key == "author":
                instance.set_author(value)
                continue

            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = ArticleModel
        fields = ['id','author','title','image','contents','output','comment_set']

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ['image']



#         class Article(models.Model):
#     author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
#     title = models.CharField('제목', max_length=50)
#     image = models.ImageField('이미지', upload_to="article/media/")
#     contents = models.TextField('내용', max_length=500)
#     output = models.ImageField('결과물', upload_to="article/media/", default='')
#     exposure_start_date = models.DateField('게시 일자',default=timezone.now())
    
    
#     def __str__(self):
#         return f"{self.author.username} 님이 작성하신 글입니다."


# class Comment(models.Model):
#     user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
#     contents = models.TextField("내용")
#     created_at = models.DateTimeField("생성시간", auto_now_add=True)
#     updated_at = models.DateTimeField("수정시간",auto_now = True)


#     def __str__(self):
#        return f"{self.user.username} 님이 작성하신 댓글입니다."