from rest_framework import serializers
from .models import Shop, ShopUser,Consumer,Payment
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

 #serializers to handle the input data for creating shop users.
class ShopUserSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = ShopUser
        fields = '__all__'
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields='__all__'
class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consumer
        fields='__all__'   
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'''

