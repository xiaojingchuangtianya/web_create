from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
#扩展用户类
class Add_User(models.Model):
    #创建User的一对一外关联,删除User会将此级联删除
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #头像上传地址,可不传图片
    head_icon = models.ImageField(upload_to="head_icon",blank=True,verbose_name="头像",default=None)
    height = models.FloatField(null=True,verbose_name="身高")
    sex = models.CharField(max_length=4,choices=(("male","男"),("female","女")),default="male",verbose_name="性别")
    school = models.CharField(max_length=20,verbose_name="就读或毕业高校",blank=True,null=True)
    description = models.CharField(max_length=200,verbose_name="用几句话来描述一下你自己吧!",null=True)


class Hot(models.Model):
    count = models.IntegerField(verbose_name="热度")
    def __str__(self):
        return str(self.count)

#博客分类
class Blog_Type(models.Model):
    #希望在博客分类进行排行,按博客类的热度进行
    type_name = models.CharField(max_length=20,verbose_name="博客分类")
    hot = models.ForeignKey(Hot,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.type_name

#博客内容类 (最好再指向一个博客分类,一个单条博客热度,方便后续的排序,以及热度推荐)
class Blog(models.Model):
    title = models.CharField(max_length=100,verbose_name="文章标题")
    write_time = models.DateTimeField(auto_now_add=True,verbose_name="写下这篇博客的时间")
    type = models.ForeignKey(Blog_Type,on_delete=models.DO_NOTHING)
    #超文本编辑框  到时候需要定义它的config_name
    content = RichTextUploadingField(config_name="blog")
    #删除使用逻辑删除,不物理删除
    is_delete = models.BooleanField(default=False)
    hot = models.ForeignKey(Hot,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.title

#博客评论类
class Comment(models.Model):
    #用自身做自己的外键
    super_comment= models.ForeignKey("self",on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=200,verbose_name="评论内容")
    created_time = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=1)
    def __str__(self):
        return self.text





