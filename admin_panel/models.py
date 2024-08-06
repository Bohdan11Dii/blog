from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ("-name",)
    
    def __str__(self) -> str:
        return self.name


class Author(AbstractUser):
    
    class Meta:
        ordering = ("username",)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    
    class Meta:
        ordering = ("title", )
    
    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    title = models.TextField()
    
    