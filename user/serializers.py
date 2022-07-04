from rest_framework import serializers

from user.models import User as UserModel
from article.serializers import ArticleSerializer, CommentSerializer

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#       #   model = UserProfile
#         fields = ["user"]

class UserSerializer(serializers.ModelSerializer):
   #  article_set = ArticleSerializer(many=True)
    #articles = ArticleSerializer(many=True, source="article_set")
   #  comment_set = CommentSerializer(many=True)
    article = ArticleSerializer(many=True, source="article_set",read_only=True)
    comment = CommentSerializer(many=True, source="comment_set",read_only=True)
    # userprofile = UserProfileSerializer()
    class Meta:
        model = UserModel
        fields = ["username","article","comment"]

from user.models import (
  User as UserModel,
  UserProfile as UserProfileModel,
  )
from article.models import (
  Comment as CommentModel,
  Article as ArticleModel,
)

class ArticleSerializer(serializers.ModelSerializer):
  article_user = serializers.SerializerMethodField()

  def get_article_user(self,obj):
    return obj.author.username
  class Meta:
    model = ArticleModel
    fields = ['id','author', 'title', 'image', 'contents', 'exposure_start_date','article_user']



class CommentSerializer(serializers.ModelSerializer):
  comments_user = serializers.SerializerMethodField()

  def get_comments_user(self,obj):
    return obj.user.username
  class Meta:
    model = CommentModel
    fields = ['comment','comments_user']


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
      model = UserProfileModel
      fields = ["username","introduction"]




class UserListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModel
    fields = ["username"]





