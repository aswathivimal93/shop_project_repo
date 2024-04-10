from shop.models import ShopUser,Shop,Consumer,Payment
from rest_framework import viewsets,permissions
from .serializers import ShopUserSerializer,ShopSerializer,ConsumerSerializer,PaymentSerializer,UserSerializer
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action



class ShopUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShopUserSerializer

    def get_queryset(self):
        return ShopUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Check if a shop user already exists for the current user
        if ShopUser.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("A shop user already exists for this user.")
        if not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create Shop.")
        
        # Extract user data from request data
        user_data = self.request.data.pop('user', {})
        
        # Set the user field of the shop user to the current user
        serializer.validated_data['user'] = self.request.user
        
        # Save shop user and user
        shop_user_instance = serializer.save()
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            shop_user_instance.delete()  # Rollback creation if user creation fails
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShopViewSet(viewsets.ModelViewSet):
    permission_classes=[
        permissions.IsAuthenticated
    ]
    serializer_class=ShopSerializer
    def get_queryset(self):
        return Shop.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create Shop.")
        serializer.save(created_by=self.request.user,updated_by=self.request.user)
    
   

class ConsumerViewSet(viewsets.ModelViewSet):
    permission_classes=[
       permissions.IsAuthenticated
    ]
    serializer_class=ConsumerSerializer
    def get_queryset(self):
        return Consumer.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        if  self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create consumer.")
        serializer.save(created_by=self.request.user,updated_by=self.request.user)



'''class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes=[
       permissions.IsAuthenticated
    ]
    serializer_class=PaymentSerializer
    def get_queryset(self):
        return Consumer.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        serializer.save()'''

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def make_payment(self, request):
        consumer_code = request.data.get('consumer_code')
        amount = request.data.get('amount')
        payment_type = request.data.get('type')
        shop_id = request.data.get('shop')  # Assuming you're passing shop ID


        try:
            consumer = Consumer.objects.get(code=consumer_code)
        except Consumer.DoesNotExist:
            return Response({"message": "Consumer not found. Please create the consumer first."}, status=status.HTTP_404_NOT_FOUND)

        if payment_type == 'debit':
            consumer.total_debit += amount
        elif payment_type == 'credit':
            consumer.total_credit+=amount
            consumer.total_debit -= amount
        consumer.save()
         # Check if there's an existing payment for the consumer
        payment = Payment.objects.filter(consumer=consumer, shop=shop_id).first()
        if payment:
            payment.amount = amount
            payment.type = payment_type
            payment.updated_by = request.user
        else:    
            payment_data = {
                'amount': amount,
                'consumer': consumer.id,
                'type': payment_type,
                'shop': shop_id,
                'created_by': request.user.id,  
                'updated_by': request.user.id
            }
            serializer = PaymentSerializer(data=payment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payment.save()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
