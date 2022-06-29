from django.db import models
from django.utils import timezone


# Create your models here.

class Article(models.Model):
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=50)
    image = models.ImageField('이미지', upload_to="article/media/")
    contents = models.TextField('내용', max_length=500)
    output = models.ImageField('결과물', upload_to="article/media/", default='')
    exposure_start_date = models.DateField('게시 일자',default=timezone.now())
    
    
    def __str__(self):
        return f"{self.author.username} 님이 작성하신 글입니다."


class Comment(models.Model):
    user = models.ForeignKey('user.User', verbose_name="사용자", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    contents = models.TextField("내용")
    created_at = models.DateTimeField("생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간",auto_now = True)


    def __str__(self):
       return f"{self.user.username} 님이 작성하신 댓글입니다."