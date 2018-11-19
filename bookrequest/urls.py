from django.conf.urls import url
from bookrequest import views

urlpatterns = [
	url(r'^book-request/$', views.BookRequestList.as_view()),
	url(r'^book-request-confirm/$', views.BookRequestConfirm.as_view()),
	url(r'^book-request-deliver/$', views.BookRequestDeliver.as_view()),
	url(r'^book-request-confirm-delivered/$', views.BookRequestConfirmDelivered.as_view()),
	url(r'^book-request-return/$', views.BookRequestReturn.as_view()),
	url(r'^book-request-confirm-returned/$', views.BookRequestConfirmReturned.as_view()),
	url(r'^book-request-reject/$', views.BookRequestReject.as_view()),
	url(r'^book-request-calification/$', views.BookRequestCalification.as_view())
]


