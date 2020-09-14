from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from data.models import Add_User,Hot,Blog_Type,Blog,Comment

#User的附加属性
class Profile_mes(admin.StackedInline):
    model = Add_User
    can_delete = False
    verbose_name = "User类的附加信息"
    fk_name = "user"

class Add_userAdmin(UserAdmin):
    inlines = (Profile_mes,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(Add_userAdmin, self).get_inline_instances(request,obj)

admin.site.unregister(User)
admin.site.register(User,Add_userAdmin)


@admin.register(Hot)
class Hot_display(admin.ModelAdmin):
    list_display = ("id","count")

@admin.register(Blog_Type)
class Blog_Type_display(admin.ModelAdmin):
    list_display = ("type_name","hot")

@admin.register(Blog)
class Blog_display(admin.ModelAdmin):
    list_display = ("title","type","write_time","is_delete","hot")
    ordering = ("-write_time",)

@admin.register(Comment)
class Comment_display(admin.ModelAdmin):
    list_display = ("text","created_time","user","super_comment")
    ordering = ("-created_time",)
