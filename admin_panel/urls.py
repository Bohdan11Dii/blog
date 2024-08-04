from django.urls import path

from admin_panel.views import index

urlpatterns = [
     path('info/', index, name='info'),
]


app_name = "admin_panel"