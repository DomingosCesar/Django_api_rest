from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


# Create your views here.
@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_users_by_nick(request, nick):
    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return  Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUSH', 'DELETE'])
def user_manager(request):
    if request.method == 'GET':
        try:
            if request.GET['user']:
                user_nickname = request.GET['user']
                try:
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # Criando Dados
    if request.method == 'POST':
        new_user = request.data
        serializer = UserSerializer(data = new_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Editando dados(PUT)
    if request.method == 'PUT':
        nickname = request.data['user_nickname']
        try:
            updater_user = User.objects.get(pk = nickname)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        print(f'data: {request.data}')

        serializer = UserSerializer(updater_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Deletar dados (DELETE)
    if request.method == 'DELETE':
        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)