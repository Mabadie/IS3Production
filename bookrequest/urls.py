from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from books import views
from bookrequest import views

urlpatterns = [
	url(r'^book-request/$', views.BookRequestList.as_view()),
	url(r'^book-request-confirm/$', views.BookRequestConfirm.as_view()),
]


