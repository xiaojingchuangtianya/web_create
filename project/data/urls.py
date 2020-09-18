from django.urls import path,re_path
from data import views
from rest_framework.routers import DefaultRouter
urlpatterns = [
    #这是获取全部数据的处理路由
    path("user/",views.UserViewSet.as_view({"get":"list","post":"deal_post"})),
    path("user/<int:pk>",views.UserViewSet.as_view({"get":"retrieve","put":"deal_put"})),

    path("blog_type/",views.Blog_TypeViewSet.as_view({"get":"list","post":"create_type"})),
    path("blog_type/<int:pk>",views.Blog_TypeViewSet.as_view({"get":"retrieve",'put':"change_hot"})),

    path("blog/",views.BlogViewSet.as_view({"get":"list","post":"create"})),
    path("blog/<int:pk>",views.BlogViewSet.as_view({"get":"retrieve","delete":"deal_delete","put":"change_blog"}))
]



