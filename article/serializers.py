from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = '__all__'

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ['image']

class CommentSerializer(serializers.ModelSerializer):
    class Meta :
        model = CommentModel
        fields = "__all__"