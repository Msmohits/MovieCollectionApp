from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


class RequestCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        all_request_count = cache.get("total_request_count", 0)
        cache.set("total_request_count", all_request_count + 1, None)
