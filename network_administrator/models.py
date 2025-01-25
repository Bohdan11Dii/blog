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
    like_count = models.IntegerField(default=0)
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
    
    def is_liked_by_user(self, user):
        """Перевіряє, чи користувач вподобав цей блог"""
        return self.likes.filter(user=user).exists()


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    anonymous_username = models.CharField(max_length=100, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ["created_time"]

    def __str__(self) -> str:
        return self.blog.title
    

class ToDoList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        null=True, blank=True
    )
    blog = models.ForeignKey(
        'Blog',
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # Унікальний ідентифікатор для незареєстрованих користувачів

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user.username} liked {self.blog.title}"


