from django.contrib import admin
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel

# Register your models here.

admin.site.register(ArticleModel)
admin.site.register(CommentModel)