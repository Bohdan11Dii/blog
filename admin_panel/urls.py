from django.urls import path

from admin_panel.views import index, GenreListView, GenreUpdateView, BlogListView, BlogDetailView

urlpatterns = [
     path("", index, name="index"),
     path("genres/", GenreListView.as_view(), name="genre-list"),
     path("genres/<int:pk>/update", GenreUpdateView.as_view(), name="genre-update"),
     path("blogs/", BlogListView.as_view(), name="blog-list"),
     path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
     
]


app_name = "admin_panel"