from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from bookrequest.serializers import BookRequestSerializer
from bookrequest.serializers import BookRequestPostSerializer
from bookrequest.serializers import BookRequestPutSerializer
from rest_framework import status
from bookrequest.models import BookRequest
from books.models import Book
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Q


class BookRequestList(APIView):
	
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		bookrequests = BookRequest.objects.filter(user= request.user.id)
		serializer = BookRequestSerializer(bookrequests, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		book=Book.objects.get(id=request.data['book'])
		request.data['user']=self.request.user.id

		serializer = BookRequestPostSerializer(data=request.data)
	
		if serializer.is_valid() and not book.owned_by(request.user):
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRequestConfirm(APIView):

	def post(self,request,format=None):
		
		serializer = BookRequestPutSerializer(data=request.data)

		if serializer.is_valid():
			try:
				bq = BookRequest.objects.get(id= request.data['id'])
				book=Book.objects.get(id=bq.book_id)
				if book.owned_by(request.user):
					bq.accept();
					return Response("Solicitud Aceptada", status=status.HTTP_200_OK)
			except:			
			
				print()
				
		return Response("", status=status.HTTP_400_BAD_REQUEST)
