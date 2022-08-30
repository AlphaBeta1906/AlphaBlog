from django import forms
from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from django.db.utils import ProgrammingError
from .models import Post, Tag,SiteSettings

# Register your models here.

class TagChoiceField(ModelChoiceField):
    
    def label_from_instance(self, obj):
        return str(obj.tag_name)

class AdminPostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdminPostForm, self).__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.all()
        self.fields['tag'].label_from_instance = lambda obj: "%s" % (obj.tag_name)
    class Meta:
        model  = Post
        fields = "__all__"

class PostAdmin(admin.ModelAdmin):
    def tag_name(self,obj):
        return obj.tag.tag_name
    form = AdminPostForm
    list_display = ("title","author","cover_image","tag","slug","date_publish","date_update","draft")
    list_filter = ("tag","draft","author")
    search_fields = ("title","tag","slug")
    date_hierarchy = "date_publish"
    exclude = ("date_update",)
    list_per_page = 10
    
class TagAdmin(admin.ModelAdmin):
    list_display = ("tag_name",)
    search_fields = ("tag_name",)
    list_per_page = 10

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_domain","site_paginate","site_author",)
    
admin.site.register(Post, PostAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(SiteSettings,SiteSettingsAdmin)
