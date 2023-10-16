'''
from django.shortcuts import render
from distutils.log import log
from functools import partial
from multiprocessing.spawn import import_main_path
from turtle import color
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PeapleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from rest_framework.decorators import action

# Create your views here.


class LoginAPI(APIView):
    def post(sefl, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    'status': False,
                    'message': serializer.errors
                }, status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'Invalid credentials'
            }, status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'status': True,
            'message': 'login success',
            'token': str(token)
        }, status.HTTP_200_OK)


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': True,
            'message': 'User created successfully'
        }, status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
def index(request):
    courses = {
        'course_name': 'Django',
        'learn': ['Models', 'Views', 'Templates', 'Admin', 'REST API'],
        'course_provider': 'Scaler',
    }

    if request.method == 'GET':
        json_response = {
            'name': 'Django',
            'courses': ['c++', 'java', 'python'],
            'method': 'GET',
        }
    else:
        data = request.data
        json_response = {
            'name': 'Django',
            'courses': ['c++', 'java', 'python'],
            'method': 'POST',
        }
    return Response(json_response)


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.data
        return Response({'message': 'login success'})
    else:
        return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # objs = Person.objects.filter(color__isnull=False)
        try:
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            pag_size = 3

            paginator = Paginator(objs, pag_size)

            serializer = PeapleSerializer(paginator.page(page), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Invalid page number'
            })
        # objs = paginator.page(page)

    def post(self, request):
        data = request.data
        serializer = PeapleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def put(self, request):
        data = request.data
        serializer = PeapleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeapleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'person deleted'})


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull=False)
        # objs = Person.objects.all()
        serializer = PeapleSerializer(objs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PeapleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeapleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'person deleted'})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeapleSerializer
    queryset = Person.objects.all()
    http_method_names = ['get', 'post']

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)

        serializer = PeapleSerializer(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def send_mail_to_person(sef, request, pk):
        obj = Person.objects.get(pk=pk)
        serializer = PeapleSerializer(obj)
        return Response({
            'status': True,
            'message': 'Email sent successfully'
        })
