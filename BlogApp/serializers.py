# from rest_framework import serializers
# from .models import Post

# class PostSerializer(serializers.ModelSerializer):   # ✅ fixed spelling
#     class Meta:
#         model = Post
#         fields = "__all__"/

from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):   # ✅ fixed spelling
    class Meta:
        model = Post
        fields = "__all__"

