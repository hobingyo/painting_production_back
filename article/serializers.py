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


class ArticlePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleModel
        fields = "__all__"

