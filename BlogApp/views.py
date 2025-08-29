from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import render
import openpyxl   # for Excel file handling

def home(request):
    return render(request, 'home.html')


# 🔹 Signup route
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )
        return Response({"message": "User created successfully"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


# 🔹 List all posts OR create a new post
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Retrieve, update, or delete a single post
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(author=3)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response({"message": "Your post has been deleted"}, status=status.HTTP_204_NO_CONTENT)


# 🔹 Bulk upload posts from Excel
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_upload_posts(request):
    excel_file = request.FILES.get("file")
    if not excel_file:
        return Response({"error": "Excel file required!"}, status=400)

    try:
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active
        created_posts = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            title, content, author_id = row

            # Get User object for ForeignKey
            try:
                author = User.objects.get(id=int(author_id))
            except User.DoesNotExist:
                return Response({"error": f"User with id {author_id} does not exist"}, status=400)

            data = {
                "title": str(title),
                "content": str(content),
                "author": author.id
            }

            serializer = PostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_posts.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        return Response({
            "message": " Posts uploaded successfully!",
            "total_uploaded": len(created_posts),
            "data": created_posts
        }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
