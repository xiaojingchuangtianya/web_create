from django.urls import path,re_path
from webrtc_use import views

urlpatterns =[
    path("first",views.first_demo),
    path("second",views.second_demo),
]
