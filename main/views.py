import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django_tables2 import RequestConfig
from .tables import UserTable
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'main/index.html', {})

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, 'main/signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, 'main/login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out!")
    return redirect("login")

@login_required
def dashboard(request):
    table = UserTable(User.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'main/dashboard.html', {'table': table})

@api_view(['GET'])
@login_required
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@login_required
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=200)
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return Response({"error": "Internal server error"}, status=500)

@api_view(['POST'])
@login_required
def update_user(request, user_id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard")
    try:
        user = User.objects.get(id=user_id)
        if request.method == "POST":
            user.username = request.POST.get("username", user.username)
            user.email = request.POST.get("email", user.email)
            user.save()
            messages.success(request, "User updated successfully!")
            return redirect("dashboard")
        return render(request, 'main/edit_user.html', {'user': user})
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("dashboard")

@api_view(['POST'])
def create_admin(request):
    if User.objects.filter(is_superuser=True).exists():
        return Response({"error": "Admin already exists"}, status=400)
    
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    user = User.objects.create_superuser(username=username, password=password)
    return Response({"message": "Admin created successfully"}, status=201)
