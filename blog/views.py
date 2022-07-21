from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage
from cms.models import Post, SiteSettings,Tag

# Create your views here.

def index(request):
    page = request.GET.get("page",1)
    paginate = 5 
    
    if SiteSettings.objects.first():
        paginate = SiteSettings.objects.first().site_paginate
    page_obj = Paginator(Post.objects.all().order_by("-id"),paginate)
    try:
        posts  = page_obj.page(page)
    except EmptyPage:
        posts = page_obj.page(page_obj.num_pages)
    return render(
        request,
        "index.html",
        {
            "posts": posts,
            "page_range": page_obj.get_elided_page_range(),
            "page_count": page_obj.count,
            "url_to": "index"
        })

def post_tag(request,tag):
    paginate = 5 
    
    if SiteSettings.objects.first():
        paginate = SiteSettings.objects.first().site_paginate  
    page = request.GET.get("page",1)
    page_obj = Paginator(Post.objects.all().filter(tag=tag).order_by("-id"),paginate)
    
    try:
        posts  = page_obj.page(page)
    except EmptyPage:
        posts = page_obj.page(page_obj.num_pages)
    return render(
        request,
        "index.html",
        {
            "posts": posts,
            "page_range": page_obj.get_elided_page_range(),
            "page_count": page_obj.count,
            "tag_page": True,
            "tag": tag,
            "url_to": "post_tag"
        })
    
def read(request,slug):
    post = Post.objects.filter(slug=slug).first()
    return render(request,"read.html",{"post": post})

def tag(request):
    paginate = 5 
    
    if SiteSettings.objects.first():
        paginate = SiteSettings.objects.first().site_paginate
    tags = Paginator(Tag.objects.all().order_by("-id"),paginate)
    return render(request,"tag.html",{"tags": tags.page(1)})

def about(request):
    _settings = SiteSettings.objects.first()
    return render(request,"about.html",{"about": _settings.site_about })

def _404(request,exception):
    return render(request,"404.html")

def _500(request):
    return render(request,"500.html")