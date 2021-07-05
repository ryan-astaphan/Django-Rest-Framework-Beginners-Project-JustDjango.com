from django.contrib.auth import get_user_model
from django.db.models import fields

from rest_framework import serializers
from .models import Post

User = get_user_model()

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username'
        )


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedIdentityField(many=False, view_name='owner_detail')

    class Meta:
        model = Post
        fields = (
            'title',
            'owner',
            'custom_id',
            'category',
            'publish_date',
            'last_updated',
            )