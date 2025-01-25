from django import forms

from network_administrator.models import Author, Blog, Genre, Comment, ToDoList


class UserRegistration(forms.ModelForm):
    
    
    class Meta:
        model = Author
        fields = ("username", "email", "password")


class BlogCreateForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        exclude = ["author"]
        

class GenreCreateForm(forms.ModelForm):
    
    class Meta:
        model = Genre
        fields = "__all__"


class CommentForm(forms.ModelForm):
    anonymous_username = forms.CharField(
        required=True,
        label="Ваш нікнейм",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Введіть нікнейм', 'class': 'name-input'}),
    )

    class Meta:
        model = Comment
        fields = ['anonymous_username', 'content']

    def clean_anonymous_username(self):
        """Перевірка, що поле з нікнеймом не заповнене, якщо користувач авторизований"""
        username = self.cleaned_data.get('anonymous_username')
        if not self.instance.user and not username:
            raise forms.ValidationError('Введіть нікнейм для анонімних користувачів.')
        return username


class ToDoForm(forms.ModelForm):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your notes"
            }
        )
    )
    class Meta:
        model = ToDoList
        fields = ("name",)
        


class BlogSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )
    )
    