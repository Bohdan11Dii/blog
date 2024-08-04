from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admin_panel.models import(
     Blog,
     Genre,
     Comment,
     Author
)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "data", "genre"]
    list_filter = ["genre", ]
    search_fields = ["title",]




admin.site.register(Genre)
admin.site.register(Author, UserAdmin)