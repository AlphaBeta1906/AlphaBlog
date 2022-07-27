from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from cms.models import  Post

class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 1
    protocol = "https"

    def items(self):
        # Return list of url names for views to include in sitemap
        return ["about","tag","index"]

    def location(self, item):
        return reverse(item)

class DynamicSitemap(Sitemap):
    changefreq = "daily"
    priority = 1
    protocol = "https"

    def items(self):
        return Post.objects.all()