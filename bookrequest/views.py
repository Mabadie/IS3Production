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
from notifications.models import Notification


class BookRequestList(APIView):
	
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format=None):
		bookrequests = BookRequest.objects.filter(Q(user= request.user.id) | Q(book__owner=request.user.id))
		serializer = BookRequestSerializer(bookrequests, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		book=Book.objects.get(id=request.data['book'])
		request.data['user']=self.request.user.id

		serializer = BookRequestPostSerializer(data=request.data)
	
		if serializer.is_valid() and not book.owned_by(request.user):
			bq=serializer.save()
			Notification.send(request.user, bq, 'alert-success', 'Solicitud(#'+str(bq.id)+'):', 'Solicitud del libro "'+book.title+'" realizada correctamente', '#')
			Notification.send(bq.book.owner, bq, 'alert-info', 'Solicitud(#'+str(bq.id)+'):', 'Tienes una solicitud  pendiente del libro "'+book.title+'"', '#')
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRequestConfirm(APIView):

	def post(self,request,format=None):
		
		serializer = BookRequestPutSerializer(data=request.data)

		if serializer.is_valid():
			try:
				bq = BookRequest.objects.get(id= request.data['id'])
				book=Book.objects.get(id=bq.book_id)
				if book.owned_by(request.user) and bq.state==0:
					bq.accept();
					Notification.send(bq.user, bq, 'alert-info', 'Solicitud(#'+str(bq.id)+'):', 'Tu solicitud del libro "'+book.title+'" fue aceptada, contacta al propietario '+book.owner.email, '#')
					Notification.send(request.user, bq, 'alert-info', 'Solicitud(#'+str(bq.id)+'):', 'Has aceptado la solicitud del libro "'+book.title+'" debes confirmar la entrega:', '#')
					return Response(status=status.HTTP_200_OK)
			except:			
			
				print()
				
		return Response("", status=status.HTTP_400_BAD_REQUEST)



class BookRequestDeliver(APIView):

	def post(self,request,format=None):

		serializer = BookRequestPutSerializer(data=request.data)

		if serializer.is_valid():
			try:
				bq = BookRequest.objects.get(id= request.data['id'])
				book=Book.objects.get(id=bq.book_id)
				if book.owned_by(request.user) and bq.state==1:
					bq.deliver()
					Notification.send(bq.user, bq, 'alert-info', 'Solicitud(#'+bq.id+'):', 'Han confirmado la entrega  del libro "'+book.title+'"; debes confirmar recepcion:', '#')
					return Response(status=status.HTTP_200_OK)
			except:

				print()

		return Response("", status=status.HTTP_400_BAD_REQUEST)





class BookRequestConfirmDelivered(APIView):

	def post(self,request,format=None):

		serializer = BookRequestPutSerializer(data=request.data)

		if serializer.is_valid():
			try:
				bq = BookRequest.objects.get(id= request.data['id'])
				if bq.user==request.user and bq.state==2:
					bq.confirm_delivered()
					Notification.send(bq.book.owner, bq, 'alert-success', 'Solicitud(#'+bq.id+'):', 'Han confirmado la recepcion  del libro "'+book.title+'"', '#')
					return Response(status=status.HTTP_200_OK)
			except:

				print()

		return Response("", status=status.HTTP_400_BAD_REQUEST)






class BookRequestReturn(APIView):

        def post(self,request,format=None):

                serializer = BookRequestPutSerializer(data=request.data)

                if serializer.is_valid():
                        try:
                                bq = BookRequest.objects.get(id= request.data['id'])
                                if bq.user==request.user and bq.state==3:
                                        bq.give_back();
                                        return Response(status=status.HTTP_200_OK)
                        except:

                                print()

                return Response("", status=status.HTTP_400_BAD_REQUEST)





class BookRequestConfirmReturned(APIView):

	def post(self,request,format=None):

		serializer = BookRequestPutSerializer(data=request.data)

		if serializer.is_valid():
			try:
				bq = BookRequest.objects.get(id= request.data['id'])
				book=Book.objects.get(id=bq.book_id)
				if book.owned_by(request.user) and bq.state==4:
					bq.confirm_return();
					return Response(status=status.HTTP_200_OK)
			except:
		
				print()

			return Response("", status=status.HTTP_400_BAD_REQUEST)



class BookRequestReject(APIView):
	
	def post(self,request,format=None):

		serializer = BookRequestPutSerializer(data=request.data)

		if serializer.is_valid():
			try:
				bq = BookRequest.objects.get(id= request.data['id'])
				book=Book.objects.get(id=bq.book_id)
				if book.owned_by(request.user) and bq.state==0:
					bq.reject();
					Notification.send(bq.user, bq, 'alert-info', 'Solicitud(#'+str(bq.id)+'):', 'Tu solicitud del libro "'+book.title+'" fue rechazada', '#')
					Notification.send(request.user, bq, 'alert-success', 'Solicitud(#'+str(bq.id)+'):', 'Has rechazado la solicitud del libro "'+book.title+'"', '#')
					return Response(status=status.HTTP_200_OK)
			except:
				print ()


		return Response("", status=status.HTTP_400_BAD_REQUEST)
