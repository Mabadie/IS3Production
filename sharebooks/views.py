#import json
#from rest_framework.views import exception_handler
#from django.http import HttpResponse

from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User


"""
def api_500_handler(exception, context):

	#response = exception_handler(exception, context)
	#if response is not None:
	response = HttpResponse(json.dumps({'error': "Algo salio mal"}),content_type="application/json", status=500)

	return response
"""

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response("Algo salio mal :(", status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user: 
        return Response("Datos no validos",status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key,'id':user.id},status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def logout(request):
	request.user.auth_token.delete();
	return Response(status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
	username = request.data.get("username")
	password = request.data.get("password")
	rpassword = request.data.get("rpassword")
	email = request.data.get("email")

	if username is None or password is None:
        	return Response("Algo salio mal :(", status=status.HTTP_400_BAD_REQUEST)

	if rpassword != password:
        	return Response("Las contraseñas no coinciden", status=status.HTTP_400_BAD_REQUEST)

	e=User.objects.filter(email=email);
	if not e is None:
		return Response("Ya existe una cuenta asociada a este email", status=status.HTTP_400_BAD_REQUEST)	
    	
	user = User.objects.create_user(username, email, password)
	user.save()

	token, _ = Token.objects.get_or_create(user=user)
	return Response({'token': token.key,'id':user.id},status=status.HTTP_200_OK)



@csrf_exempt
def home(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render({}, request))
