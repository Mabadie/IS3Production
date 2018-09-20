from django.shortcuts import render

# Create your views here.


from django.views.decorators.csrf import csrf_exempt
from books.models import Book
from books.serializers import BookSerializer
from books.serializers import BookPostSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db.models import Q

#@csrf_exempt

class BookList(APIView):

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)	

	def get(self, request, format=None):
        	books = Book.objects.filter(~Q(owner = self.request.user.id))
	        serializer = BookSerializer(books, many=True)
        	return Response(serializer.data)
	
 

class MyBookList(APIView):

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)	

	def get(self, request, format=None):
        	books = Book.objects.filter(owner=self.request.user.id)
	        serializer = BookSerializer(books, many=True)
        	return Response(serializer.data)

	def post(self, request, format=None):
		request.data['owner']=request.user.id
		serializer = BookPostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response("", status=status.HTTP_201_CREATED)
		return Response("", status=status.HTTP_400_BAD_REQUEST)


	
class BookDetail(APIView):
	
	permission_classes = (permissions.IsAuthenticatedOrReadOnly)
	
	def get(self, request, id,format=None):
		try:
			book = Book.objects.get(id=id)
		except Book.DoesNotExist:
			return Response("", status=status.HTTP_400_BAD_REQUEST)
		serializer = BookSerializer(book)
		return  Response(serializer.data)



