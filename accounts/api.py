from rest_framework import generics,permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer,RegisteSerializer,LoginSerializer

#Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data
        #token = AuthToken.objects.create(user)[1] 
        return Response({"user":UserSerializer(user,context=self.get_serializer_context()).data,
                         "token":AuthToken.objects.create(user)[1]})  