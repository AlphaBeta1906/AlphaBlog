from django.urls import path 
from django.conf.urls import handler404,handler500
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("read/<slug:slug>",views.read,name="read_post"),
    path("t/<str:tag>",views.post_tag,name="post_tag"),
    path("t/",views.tag,name="tag"),
    path("about",views.about ,name="about")
]

handler404 = views._404
handler500 = views._500