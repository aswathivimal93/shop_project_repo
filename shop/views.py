from django.shortcuts import render

'''from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import ShopUserSerializer ,CustomUserLoginSerializer,ShopSerializer,ConsumerSerializer,PaymentSerializer
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from knox.auth import AuthToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token




#views for creating shop users.
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_shop_user(request):
    if request.method == 'POST':
        serializer = ShopUserSerializer(data=request.data)
        if serializer.is_valid():
            shop_user=serializer.save()
            response_data = {
                'username': shop_user.user.username,
                'phone': shop_user.phone,
                'email': shop_user.email,
                'password':shop_user.user.password,     
                'total_collection': shop_user.total_collection
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_shop(request):
    if request.method == 'POST':
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
#@permission_classes([IsAuthenticated])  # Ensure only authenticated users (shop users) can access these endpoints
def create_consumer(request):
    if request.method == 'POST':
        serializer = ConsumerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])  # Assuming shop users need to be authenticated
def create_payment(request):
    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class CustomLoginView(KnoxLoginView):
    permission_classes = [] 
    def post(self, request, format=None):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if user.is_superuser or hasattr(user, 'shopuser'):
            token = Token.objects.create(user)[1]  # Generating token
            
            return Response({
                'user_id': user.pk,
                'user_username': user.username,
                'token': token
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only superusers or ShopUsers are allowed to log in.'}, status=status.HTTP_403_FORBIDDEN)
    def post(self, request, format=None):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_superuser:
           # token = AuthToken.objects.create(request.user)[1]
            token = AuthToken.objects.create(user)[1] 
            

            return Response({'user_id': user.pk, 
                             'user_username': user.username,
                             'token': token
                             }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only superusers are allowed to log in.'}, status=status.HTTP_403_FORBIDDEN)
    
class CustomLogoutView(KnoxLogoutView):
    permission_classes = [IsAuthenticated]  '''
