from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import APIView
from rest_framework import viewsets
from app.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import HTMLFormRenderer, MultiPartRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework import status
import json
import celery
from rest_framework.throttling import ScopedRateThrottle
class custompagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class BookListCreateAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = custompagination
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-id')
        # book = self.request.query_params.get("book", None)
        # if book:
        #     queryset = queryset.filter(book_name__icontains=book)
        
        return queryset
class BookDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # lookup_fields = ['pk', 'price']
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwargs = {}
        for lookup_field in self.lookup_fields:
            value = self.kwargs.get(lookup_field, None)
            if value is not None:
                lookup_url_kwargs[lookup_field] = value
        obj = get_object_or_404(queryset, **lookup_url_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj            
    
class register(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            User.objects.create(username=serializer.validated_data['username'],
                                password=make_password(serializer.validated_data['password']),
                                email=serializer.validated_data['email'])
            
            message = {
                "data": serializer.data,
                "message": "User created successfully"
            }
            
            return Response(data = message, status = status.HTTP_201_CREATED)
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                login(request, user)
                message = {
                    "data": serializer.data,
                    "message": "User logged in successfully"
                }
                return Response(data=message, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)
        data = data.data
        data = {
            "data" : data,
            "message" : "Received data successfully"
        }
        return Response(data)
    
    @action(methods=['get'], detail=False)
    def featured(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
@method_decorator(cache_page(60 * 60 * 2))
def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)