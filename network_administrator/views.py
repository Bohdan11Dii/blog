from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.views import View
from django.http import JsonResponse
from network_administrator.forms import UserRegistration, BlogCreateForm, GenreCreateForm, CommentForm, ToDoForm, BlogSearchForm
from network_administrator.models import Blog, Genre, Comment, Author, Like, ToDoList




def web_site(request: HttpResponse) -> HttpRequest:
    filter_type = request.GET.get("filter", "all")  # За замовчуванням показуємо загальні блоги

    if request.user.is_authenticated:
        if filter_type == "my":  # Мої блоги
            blogs = Blog.objects.filter(author=request.user)
        else:  # Загальні блоги
            blogs = Blog.objects.all()
    else:
        # Для анонімних користувачів завжди показуємо всі блоги
        blogs = Blog.objects.all()

    context = {
        "blogs": blogs,
        "filter_type": filter_type,  # Передаємо фільтр у шаблон
    }
    return render(request, "web_site/web_site.html", context=context)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_blogs = Blog.objects.count()
    num_genres = Genre.objects.count()
    num_comments = Comment.objects.count()
    users = Author.objects.all()
    to_do_list = ToDoList.objects.filter(user=request.user)
    form = ToDoForm()
    context = {
        "num_blogs": num_blogs,
        "num_genres": num_genres,
        "num_comments": num_comments,
        "users": users,
        'to_do_list': to_do_list, 
        'form': form

    }

    return render(request, "network_administrator/index.html", context=context)


class CreateUserView(generic.CreateView):
    form_class = UserRegistration
    template_name = 'registration/register.html'
    success_url = reverse_lazy("network_administrator:index")

    def form_valid(self, form):
        # Створюємо користувача за допомогою форми
        user = form.save()
        
        password = form.cleaned_data.get('password') 
        user.set_password(password)  # Хешуємо пароль перед збереженням
        
        # Автоматичний логін користувача після реєстрації
        login(self.request, user)

        # Переходимо на сторінку після успішної реєстрації
        return super().form_valid(form)
    

#CRUD for Genre
class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    paginate_by = 10
    
    def get_queryset(self):
        """Return blogs authored by the current user."""
        return Genre.objects.filter(blogs__author=self.request.user).distinct()


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    form_class = GenreCreateForm
    success_url = reverse_lazy("network_administrator:genre-list")


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    form_class = GenreCreateForm
    success_url = reverse_lazy("network_administrator:genre-list")


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("network_administrator:genre-list")


#CRUD for Blog
class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
   
    paginate_by = 10

    def get_queryset(self):
        queryset = Blog.objects.filter(author=self.request.user).select_related("genre")
        form = BlogSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")
        context["search_form"] = BlogSearchForm(
            initial={
                "title": title
            }
        )
        return context
   

class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    model = Blog


class BlogCreteView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy("network_administrator:blog-list")
    
    def form_valid(self, form):
        # Передаємо користувача у метод save форми
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy("network_administrator:blog-list")


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    success_url = reverse_lazy("network_administrator:blog-list")


class StoryDetailView(generic.DetailView):
    model = Blog
    template_name = "web_site/story_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()  # Отримуємо блог
        # Створюємо форму для коментаря і передаємо в контекст
        user = self.request.user
        context['is_liked'] = blog.is_liked_by_user(user) if user.is_authenticated else False
        context['form'] = CommentForm()  
        context['comments'] = blog.comment_set.all()
        return context
    
#CREATE COMMENT 
class CommentaryCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Видаляємо поле нікнейму для авторизованих користувачів
        if self.request.user.is_authenticated:
            form.fields.pop('anonymous_username', None)
        return form

    def form_valid(self, form):
        blog = get_object_or_404(Blog, pk=self.kwargs.get("pk"))
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user = None
            form.instance.anonymous_username = form.cleaned_data.get('anonymous_username')
        form.instance.blog = blog
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("network_administrator:story-detail", kwargs={"pk": self.kwargs["pk"]})

#CREATE TODOLIST
class ToDoCreateView(LoginRequiredMixin, generic.CreateView):
    model = ToDoList
    form_class = ToDoForm
    context_object_name = "to_do"
    
    def form_valid(self, form):
        # Зберігаємо новий елемент ToDoList
        form.instance.user = self.request.user
        to_do = form.save()

        # Повертаємо JSON-відповідь для AJAX-запиту
        return JsonResponse({'id': to_do.id, 'name': to_do.name}, status=200)

    def form_invalid(self, form):
        # Якщо форма невалідна, повертаємо помилки у JSON-форматі
        return JsonResponse({'errors': form.errors}, status=400)

    def get_success_url(self):
        return reverse_lazy("network_administrator:index")

    @method_decorator(csrf_exempt)  # Якщо виникають проблеми з CSRF
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ToDoDeleteView(LoginRequiredMixin, View):
    model = ToDoList
    context_object_name = 'to_do'
    success_url = reverse_lazy("network_administrator:index")
    
    def get_queryset(self):
        # Ensure that the user can only delete their own to-do list items
        return ToDoList.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Get the to-do item
        try:
            to_do = get_object_or_404(ToDoList, id=kwargs['pk'], user=request.user)
            to_do_name = to_do.name
            to_do.delete()
            return JsonResponse({'message': f'Task "{to_do_name}" deleted successfully.'}, status=200)
        except ToDoList.DoesNotExist:
            return JsonResponse({'error': 'Task not found or unauthorized.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

#CREATE LIKE BLOG
class ToggleLikeView(View):
    def post(self, request, blog_id):
        # Отримуємо об'єкт блогу
        blog = Blog.objects.get(id=blog_id)

        # Ідентифікуємо користувача
        if request.user.is_authenticated:
            user = request.user
            like = Like.objects.filter(blog=blog, user=user).first()
        else:
            # Для незареєстрованих використовуємо session_id
            session_id = request.session.get('session_id')
            if not session_id:
                session_id = get_random_string(32)
                request.session['session_id'] = session_id

            like = Like.objects.filter(blog=blog, session_id=session_id).first()

        # Тогл лайка
        if like:
            like.delete()
            blog.like_count -= 1  # Правильний доступ до поля
            blog.save()
            return JsonResponse({'liked': False, 'like_count': blog.like_count})
        else:
            Like.objects.create(
                blog=blog,
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.get('session_id')
            )
            blog.like_count += 1  # Правильний доступ до поля
            blog.save()
            return JsonResponse({'liked': True, 'like_count': blog.like_count})