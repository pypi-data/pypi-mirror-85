from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse

class LatestPostsFeed(Feed):
    title = "Cheap Local Websites Blog"
    link = ""
    description = "New posts weekly."

    def items(self):
        return Post.objects.all().order_by("-published")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)