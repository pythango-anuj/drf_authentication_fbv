from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status
from django.db import IntegrityError
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from .serializers import CustomUserSerializer
import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# CUSTOM AUTHENTICATION THROUGH FUNCTION BASED VIEWS:

# To list all the Registered Users:
@swagger_auto_schema(method=['GET'])
@api_view(["GET"])
@permission_classes([IsAdminUser])
def all_users(request):
    users = CustomUser.objects.all()
    data = CustomUserSerializer(users, many=True).data
    if data:
        return Response(data=data)
    else:
        data = dict()
        data['message'] = "No Registered user available !!"
        return Response(data=data)

# Registering a CustomUser manually:
@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'dob': openapi.Schema(type=openapi.TYPE_STRING, description='DOB'),
        'phone_no': openapi.Schema(type=openapi.TYPE_STRING, description='Phone No'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
        'is_staff': openapi.Schema(type=openapi.TYPE_STRING, description='Staff Status'),
    }
))
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    try:
        data = request.data
        res={}
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            res["message"] = "user registered successfully"
            res["username"] = account.username
        else:
            data = serializer.errors
        return Response(res)

    except IntegrityError as e:
        account = CustomUser.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})


# TO GET LOGGED IN:
@swagger_auto_schema(method='POST', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    }

))
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    reqBody = json.loads(request.body)
    username = reqBody['username']
    password = reqBody['password']
    try:
        account = CustomUser.objects.get(username=username)
    except BaseException as e:
        raise ValidationError({"400": f'{str(e)}'})

    token = Token.objects.get_or_create(user=account)[0].key
    print(token)
    if not check_password(password, account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})

    if account:
        if account.is_active:
            login(request, account)
            print(request.user)
            data["message"] = "user logged in"
            data["username"] = account.username

            Res = {"data": data, "token": token}

            return Response(Res)

        else:
            raise ValidationError({"400": f'Account not active'})

    else:
        raise ValidationError({"400": f'Account doesnt exist'})

# TO GET LOGGED OUT:
@swagger_auto_schema(method=['GET'])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    #Token.objects.all().filter(user=request.user.id).delete()
    #request.user.auth_token.delete()
    #request.user.onetoone.delete()
    #token=Token.objects.get_or_create(user=request.user)[0]
    #token.delete()
    #request.user.refresh_from_db
    logout(request)
    data = {'success': 'Sucessfully logged out'}
    return Response(data = data, status=status.HTTP_200_OK)
