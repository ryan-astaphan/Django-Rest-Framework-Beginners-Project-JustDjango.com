from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView

from .models import Post
from .serializers import PostSerializer

def home(request):
    return render(request, "index.html")

class PostListView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
