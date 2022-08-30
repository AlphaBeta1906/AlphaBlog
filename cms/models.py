from io import BytesIO
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.files import File
from autoslug import AutoSlugField
from markdownx.models import MarkdownxField
from PIL import Image


def compress(image):
    import random
    img = Image.open(image)
    img_io = BytesIO()
    img.save(img_io,format="webp",quality=60,optimize=True)
    new_img = File(img_io,name=''.join(chr(random.randrange(65,90)) for i in range(10)) + ".webp")
    return new_img
    
class SiteSettings(models.Model):
    site_description = models.TextField(max_length=150,null=False)
    site_domain = models.CharField(max_length=100,null=False)
    site_paginate = models.PositiveIntegerField(default=5,validators=[MaxValueValidator(10),MinValueValidator(3)])
    site_about = models.TextField(max_length=150,null=False)
    site_author = models.CharField(max_length=50,default="salman",editable=False)

class Tag(models.Model):
    tag_name = models.CharField(max_length=50,null=False,unique=True)
    description = models.TextField(max_length=150,null=False)
    def __str__(self):
        return f"{self.tag_name}"


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=False,db_column="user")
    title =  models.CharField(null=False,max_length=50)
    content = MarkdownxField()    
    cover_image = models.ImageField(upload_to="static/image",default="static/image/nopic.png")
    date_publish = models.DateField(auto_now=True, editable=False)
    date_update = models.DateField(null=True)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,null=False)
    slug = AutoSlugField(populate_from="title" )
    draft = models.BooleanField(default=False,null=False)
    
    def save(self,*args, **kwargs):
        self.cover_image = compress(self.cover_image)
        exist = Post.objects.filter(title=self.title).first()
        if not self.draft and exist:
            self.date_update = timezone.now()
        return super(Post,self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("read_post", kwargs={"slug": self.slug})
    
