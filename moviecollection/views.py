from django.shortcuts import render
import requests, os
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from .models import Movie, Collection, User
from .serializers import UserSerializer, MovieSerializer, CollectionSerializer
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .resolvers import third_part_api_handler


@api_view(["POST"])
def register(request):
    data = json.loads(request.body)
    try:
        user = User.objects.create(**data)
        refresh = RefreshToken.for_user(user)
        return JsonResponse(
            {
                "access_token": str(refresh.access_token),
                # 'refresh_token': str(refresh),
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["POST"])
def login(request):
    data = json.loads(request.body)
    try:
        user = User.objects.filter(username=data.get("username")).first()
        refresh = RefreshToken.for_user(user)
        return JsonResponse(
            {
                "access_token": str(refresh.access_token),
                # 'refresh_token': str(refresh),
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users(request):
    users = User.objects.values()
    # serializer = UserSerializer(users, many=True)
    return Response(users)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def collction_movies(request):
    movies = Movie.objects.prefetch_related("collection_set")
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def movie_list(request, page):
    response = third_part_api_handler(page)
    return response


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def collection_list(request):
    if request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            collection = serializer.save(user=request.user)
            return Response(
                {"collection_id": collection.id}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        collections = Collection.objects.filter(user=request.user)
        # collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(
            {"is_success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


@api_view(["PUT", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def collection_detail(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id, user=request.user)
    except Collection.DoesNotExist:
        return Response(
            {"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def request_count(request):
    all_request_count = cache.get("total_request_count", 0)
    return Response(
        {
            "all_requests_count": all_request_count,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reset_request_count(request):
    cache.set("total_request_count", 0, None)
    return Response(
        {"message": "Request count reset successfully"}, status=status.HTTP_200_OK
    )
