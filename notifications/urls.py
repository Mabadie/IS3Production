from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from notifications import views

urlpatterns = [
        url(r'^notifications/$', views.NotificationsList.as_view()),
]

