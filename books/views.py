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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db.models import Q


# @csrf_exempt

class BookList(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        books = Book.objects.filter(~Q(owner=self.request.user.id))

        if request.GET.get('search'):
            books = books.filter(title__icontains=self.request.GET['search'])
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class MyBookList(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        books = Book.objects.filter(owner=self.request.user.id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['owner'] = request.user.id
        serializer = BookPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("", status=status.HTTP_201_CREATED)
        return Response("", status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    def get(self, request, id, format=None):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(book)
        return Response(serializer.data)

# {"owner": "jcarbajales", "title":"Pateando lunas", "author":"Helen Belando, "year":"1992", "image":"estoesunaimagen"}


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def insert(request):
    owner = request.data.get("owner")
    title = request.data.get("title")
    author = request.data.get("author")
    year = request.data.get("year")
    image = request.data.get("image")

    if User.objects.filter(username=owner).exists():
        book = Book(owner=User.objects.get(username=owner), title=title, author=author,
                    year=year, image=image, aviable=True)
        book.save()
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
    else:
        return Response("Algo salio mal :(", status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def update(request):
    id = request.data.get("id")
    #owner = request.data.get("owner") #Supongo que no se actualiza, al igual que 'aviable' pero por las dudas lo dejé
    title = request.data.get("title")
    author = request.data.get("author")
    year = request.data.get("year")
    image = request.data.get("image")
    #aviable = request.data.get("aviable")

    if Book.objects.filter(id=id).exists():
        book = Book.objects.get(id=id)
        #book.owner = owner
        book.title = title
        book.author = author
        book.year = year
        book.image = image
     #   book.aviable = aviable
        book.save()
        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
    else:
        return Response("Algo salio mal :(", status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def delete(request):
    print (request.data.get("id"))
    id = request.data.get("id")

    if Book.objects.filter(id=id).exists():
        book = Book.objects.get(id=id)
        book.delete()
        return Response("Libro eliminado.", status=status.HTTP_202_ACCEPTED)
    else:
        return Response("Algo salio mal :(", status=status.HTTP_400_BAD_REQUEST)
