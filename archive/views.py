from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT, 
    HTTP_400_BAD_REQUEST,
)

from .models import Post
from .permissions import IsOwnerPermission
from .serializers import PostSerializer, OwnerSerializer

# Create your views here.
User = get_user_model()

class PostView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)


@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = PostSerializer (data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)


class PostMixinListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwnerPermission)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class OwnerDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = OwnerSerializer


