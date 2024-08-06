from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from admin_panel.models import Blog, Genre, Comment, Author

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    num_blogs = Blog.objects.count()
    num_genres = Genre.objects.count()
    num_comments = Comment.objects.count()
    users = Author.objects.all()

    context = {
        "num_blogs": num_blogs,
        "num_genres": num_genres,
        "num_comments": num_comments,
        "users": users,

    }

    return render(request, "admin_panel/index.html", context=context)


class GenreListView(generic.ListView):
    model = Genre


class GenreUpdateView(generic.UpdateView):
    model = Genre
    fields = "__all__"

class BlogListView(generic.ListView):
    model = Blog
    queryset = Blog.objects.select_related("genre")


class BlogDetailView(generic.DetailView):
    model = Blog
    

