from django.contrib import admin
from blog.models import Post, Author

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'author')
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Author)