from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets #视图集
from rest_framework.response import Response #这是响应
from django.contrib.auth.models import User
from data.models import Add_User,Hot,Blog_Type,Blog,Comment
from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView#这些是二级视图类
from data.serializers import UserSerializer,Add_UserSerializer,HotSerializer,Blog_TypeSerializer,BlogSerializer,CommentSerializer#引入序列化器

"""
    业务没有大量的自定义视图,使用三级视图来解决
常见的三级视图:
类名                 父类                                   提供的方法,功能            作用
(列表视图)
ListAPIView       GenericAPIView,ListModelMixin             get              查询所有数据
CreateAPIView     GenericAPIView,CreateModelMixin           post             创建单个对象
(详情视图)
RetrieveAPIView   GenericAPIView,RetrieveModelView          get              获取单个数据
DestroyAPIView    GenericAPIView,DestroyModelView           delete           删除单个数据
UpdateAPIView     GenericAPIView,UpdateModelView            put              修改单个数据
"""
#用户数据
#继承视图集View_Set,  后续应该设置权限,为管理员专用
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
#列表视图
    def list(self,request):
        serializer = UserSerializer(self.queryset,many=True)
        return Response(serializer.data)

    # 无法用drf的接口来进行数据写入,只能靠django的来写入
    def deal_post(self, request):
        user_serializer = UserSerializer(data=request.data)
        add_serializer = Add_UserSerializer(data=request.data["add_user"])
        if user_serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(request.data["username"], request.data["email"], request.data["password"])
            user_id = User.objects.get(username=user).id
            # 如果用户生成完毕,则添加用户额外的数据
            if add_serializer.is_valid(raise_exception=True):
                Add_User.objects.create(user_id=user_id, **request.data["add_user"])
            return Response({"message": "用户" + request.data["username"] + "创建成功!"}, status=201)

#详情视图
    #根据id获取单个用户
    def retrieve(self,request,pk=None):
        single =get_object_or_404(self.queryset,pk=pk)
        user_serializer = UserSerializer(single)
        return Response(user_serializer.data)

#处理上传问题等还存在一些问题,后续再继续优化
    def deal_put(self,request,pk=None):
        data_dict = request.data
        adduser_serializer = Add_UserSerializer(data=data_dict["add_user"])
        if adduser_serializer.is_valid(raise_exception=True):
            #更新图片需要传入一个图片文件的内容,而不是一个文本链接,后续再更改
            Add_User.objects.filter(user_id=pk).update(**data_dict["add_user"])
            del request.data["add_user"]
        user_serializer = UserSerializer(data=data_dict)
        if user_serializer.is_valid(raise_exception=True):
            User.objects.filter(pk=pk).update(**data_dict)
        return Response("成功了")

#博客分类
class Blog_TypeViewSet(viewsets.ViewSet):
    queryset = Blog_Type.objects.all()
    def list(self,reuqest):
        serializer = Blog_TypeSerializer(instance=self.queryset,many=True)
        return Response(serializer.data)
    #每次添加,返回一个type_name即可,而不需要返回热度,
    def create_type(self,request):
        hot = Hot.objects.create()#创建type时会连带创建它的hot外表元组
        blog_type=Blog_Type.objects.create(**request.data,hot=hot)
        return Response("typename"+blog_type+" is now created")

    def retrieve(self,request,pk=None):
        single = get_object_or_404(self.queryset,pk=pk)
        blog_typeSerialzier = Blog_TypeSerializer(single)
        return Response(blog_typeSerialzier.data)

#用ContentType
    def change_hot(self,request,pk=None):
        contentype=ContentType.objects.get(app_label="data",model="blog_type")
        try:
            get_object=contentype.model_class().objects.get(pk=pk)
            get_object.hot.count +=1
            get_object.hot.save()
        except Exception as e:
            return Response({"error":"数据不是合理范围","exception":str(e)})
        return Response({"修改数据":"success"})

class BlogViewSet(viewsets.ViewSet):
    queryset = Blog.objects.all()
    def list(self,request):
        serializer = BlogSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self,request):
        #需要判别type是否存在,不存在新建,存在则连接
        if Blog_Type.objects.filter(type_name=request.data["type"]):
            blog_type=Blog_Type.objects.get(type_name=request.data["type"])
        else:
            hot=Hot.objects.create()#这里的hot是指向类的hot
            blog_type=Blog_Type.objects.create(type_name=request.data["type"],hot=hot)
        hot = Hot.objects.create() #每次自动新建一个hot外部关联\
        request.data["type"]=blog_type
        Blog.objects.create(**request.data,hot=hot)
        return Response("asd")

    def retrieve(self,request,pk):
        blog = Blog.objects.filter(pk=pk)[0]
        BlogSer = BlogSerializer(instance=blog)
        return Response(BlogSer.data)

    def deal_delete(self,request,pk):
        #调用此接口,会将数据的is_delete转为True,逻辑删除数据
        blog=Blog.objects.get(pk=pk)
        blog.is_delete=True
        blog.save()
        BlogSer = BlogSerializer(instance=blog)
        return Response(BlogSer.data)

    def change_blog(self,request,pk):
        #这个接口允许修改标题,文章,作者(不存在不允许此处生成),分类(不存在可创建新分类)
        try:
            if Blog_Type.objects.filter(type_name=request.data["type"]):
                blog_type=Blog_Type.objects.get(type_name=request.data["type"])
            else:
                hot=Hot.objects.create()#这里的hot是指向类的hot
                blog_type=Blog_Type.objects.create(type_name=request.data["type"],hot=hot)
            request.data["type"]=blog_type
        except Exception as e:
            pass

        try:
            request.data["user"]=User.objects.get(username=request.data["user"])
        except Exception as e:
            print(e)
            return Response("用户不存在,不允许修改用户为不存在的用户")

        change_blog = Blog.objects.filter(pk=pk)  # 获取博客
        change_blog.update(**request.data)
        blog = Blog.objects.get(pk=pk)
        blogserializer =BlogSerializer(instance=blog)
        return Response(blogserializer.data)

#获取评论的话,应该依据单条博客来获取,暂时先不需要,因为模型字段不足,还有处理逻辑出错
class CommentViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset =Comment.objects.all()
