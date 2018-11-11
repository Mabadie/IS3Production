from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from books import views
from books.views import insert, update, delete


urlpatterns = [
    url(r'^books/$', views.BookList.as_view()),
    url(r'^books/(?P<search>[A-Za-z]+)/$', views.BookList.as_view()),
    url(r'^my-books/(?P<id>[0-9]+)/$', views.BookDetail.as_view()),
    url(r'^my-books/$', views.MyBookList.as_view()),
    path('my-books/insert/', insert),
    path('my-books/update/', update),
    path('my-books/delete/', delete)
]
