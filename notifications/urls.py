from django.conf.urls import url
from notifications import views

urlpatterns = [
        url(r'^notifications/$', views.NotificationsList.as_view()),
]

