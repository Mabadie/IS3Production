#import json
#from rest_framework.views import exception_handler
#from django.http import HttpResponse

from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

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
        return Response("",status=status.HTTP_400_BAB_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=status.HTTP_200_OK)


