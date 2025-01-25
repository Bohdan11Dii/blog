from django.urls import path

from network_administrator.views import(
      web_site,
      index,
      GenreListView,
      GenreCreateView,
      GenreUpdateView,
      GenreDeleteView,
      
      BlogListView,
      BlogDetailView,
      BlogCreteView,
      BlogUpdateView,
      BlogDeleteView,
      
      CommentaryCreateView,
      
      StoryDetailView,
      
      ToDoCreateView,
      ToDoDeleteView,
      
      ToggleLikeView,
      
      CreateUserView,
)

urlpatterns = [
     path("", web_site, name="web-site"),
     path("home", index, name="index"),
     
     path("genres/", GenreListView.as_view(), name="genre-list"),
     path("genres/create/", GenreCreateView.as_view(), name="genre-create"),
     path("genres/<int:pk>/update", GenreUpdateView.as_view(), name="genre-update"),
     path("genres/<int:pk>/delete", GenreDeleteView.as_view(), name="genre-delete"),
     
     path("blogs/", BlogListView.as_view(), name="blog-list"),
     path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
     path("blogs/create/", BlogCreteView.as_view(), name="blog-create"),
     path("blogs/<int:pk>/update/", BlogUpdateView.as_view(), name="blog-update"),
     path("blogs/<int:pk>/delete/", BlogDeleteView.as_view(), name="blog-delete"),
     
     path("stories/<int:pk>/", StoryDetailView.as_view(), name="story-detail"),
     
     path('stories/<int:pk>/comment/', CommentaryCreateView.as_view(), name='commentary-create'),
     
     path("home/to_do", ToDoCreateView.as_view(), name="create-todo"),
     path('home/delete-todo/<int:pk>/', ToDoDeleteView.as_view(), name='delete-todo'),
     
     path('blog/<int:blog_id>/toggle-like/', ToggleLikeView.as_view(), name='toggle_like'),
      
     path("registration/", CreateUserView.as_view(), name="registration"),
     
     
]


app_name = "network_administrator"