from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from Users.serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.
class Users(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request):
        user = User.objects.get(id=request.data['userId'])

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request):
        user = User.objects.get(id=request.data['userId'])

        if request.data['type']=='name':
            user.username = request.data['username']
        elif request.data['type'] == 'email':
            user.email = request.data['email']
        else:
            if user.check_password(request.data['actualPassword']):
                if request.data['password']==request.data['rpassword']:
                    user.set_password(request.data['password'])
                    user.save()
                else:
                    return Response({"message":"Las contraseñas no coinciden"},500)
            else:
                return Response({"message":"La contraseña no es correcta"},500)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)