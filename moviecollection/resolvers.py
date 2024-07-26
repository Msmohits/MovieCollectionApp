import requests
import os
from django.http import JsonResponse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rest_framework.response import Response
from django.core.cache import cache


def third_part_api_handler(page):
    username = os.environ.get("username")
    password = os.environ.get("password")
    retry_strategy = Retry(
        total=3,  # Number of retries
        backoff_factor=1,  # Backoff factor (delay between retries)
        status_forcelist=[301, 500, 502, 503, 504],  # Status codes that trigger retry
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Create a session and mount the adapter
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    try:
        response = session.get(
            f"https://demo.credy.in/api/v1/maya/movies/?page={page}",
            auth=(username, password),
            verify=False,
        )
        return Response(response.json())
    except Exception as e:
        return JsonResponse({"error": str(e)})


def remove_password_deco(func):
    def inner(request):
        response = func(request)
        for user in response.data:
            if 'password' in user:
                del user['password']
        return response
    return inner

