from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from autoslug import AutoSlugField
from markdownx.models import MarkdownxField

class SiteSettings(models.Model):
    site_description = models.TextField(max_length=150,null=False)
    site_domain = models.CharField(max_length=100,null=False)
    site_paginate = models.PositiveIntegerField(default=5,validators=[MaxValueValidator(10),MinValueValidator(3)])
    site_about = models.TextField(max_length=150,null=False)
    site_author = models.CharField(max_length=50,default="salman",editable=False)

class Tag(models.Model):
    tag_name = models.CharField(max_length=50,null=False,unique=True)
    description = models.TextField(max_length=150,null=False)

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,db_column="user")
    title =  models.CharField(null=False,max_length=50)
    content = MarkdownxField(max_length=10000000)
    cover_image = models.ImageField(upload_to="static/image",default="static/image/nopic.png")
    date_publish = models.DateField(auto_now=True, editable=False)
    date_update = models.DateField(null=True)
    tag = models.CharField(null=False,max_length=50)
    slug = AutoSlugField(populate_from="title" )
    draft = models.BooleanField(default=False,null=False)
    
    def save(self,*args, **kwargs):
        if self.date_publish:
            self.date_update = timezone.now()
        super(Post,self).save(*args, **kwargs)