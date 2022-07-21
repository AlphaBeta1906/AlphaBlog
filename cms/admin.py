from django import forms
from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from django.db.utils import ProgrammingError
from .models import Post, Tag,SiteSettings
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class TagChoiceField(ModelChoiceField):
    
    def label_from_instance(self, obj):
        return str(obj.tag_name)

class AdminPostForm(ModelForm):
    tag = forms.ChoiceField(choices=[])
    def __init__(self, *args, **kwargs):
        try:
            _tags = [(_tag["tag_name"],_tag["tag_name"]) for _tag in Tag.objects.values("tag_name")]
        except ProgrammingError:
            _tags = [("","")]    
        super(AdminPostForm, self).__init__(*args, **kwargs)
        self.fields['tag'].choices = _tags
    
    class Meta:
        model  = Post
        fields = ("author","title","content","cover_image","date_update","tag","draft")

class PostAdmin(SummernoteModelAdmin):
    form = AdminPostForm
    list_display = ("title","author","tag","slug","date_publish","date_update","draft")
    summernote_fields = ("content",)
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