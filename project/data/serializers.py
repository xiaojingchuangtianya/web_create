from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from data.models import Add_User,Hot,Blog_Type,Blog,Comment

class Add_UserSerializer(ModelSerializer):
    class Meta:
        model = Add_User
        fields = ["head_icon","height","sex","school","description"]

class UserSerializer(ModelSerializer):
    add_user=Add_UserSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["username","email","date_joined","add_user"]
        write_only_fields =['password']


class HotSerializer(ModelSerializer):
    class Meta:
        model =Hot
        fields =["count"]

class Blog_TypeSerializer(ModelSerializer):
    hot =HotSerializer()
    class Meta:
        model =Blog_Type
        fields=["type_name","hot"]

class BlogSerializer(ModelSerializer):
    user =UserSerializer()
    hot =HotSerializer()
    type =Blog_TypeSerializer()
    class Meta:
        model =Blog
        fields=["title","write_time","content","is_delete","type","user","hot"]

class CommentSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ["text","created_time","user"]



