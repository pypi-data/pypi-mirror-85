from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, unique=True)
    img = models.ImageField(upload_to='uploads/posts')
    description = models.TextField(max_length=100)
    body = models.TextField()
    published = models.DateField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
