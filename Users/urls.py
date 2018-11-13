from django.conf.urls import url
from Users import views

urlpatterns = [
    url(r'^getUser/$', views.Users.as_view()),
]
