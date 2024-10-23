#!/usr/bin/env python3
"""
Caching request module with tracking and expiration
"""
from functools import wraps
from typing import Callable
import requests
import redis
import hashlib

# Constant for cache expiration time (10 seconds)
CACHE_EXPIRATION = 10

# Create a global Redis client instance
redis_client = redis.Redis()

def sanitize_url(url: str) -> str:
    """Generates a Redis-friendly key by hashing the URL."""
    return hashlib.md5(url.encode()).hexdigest()

def track_get_page(fn: Callable) -> Callable:
    """Decorator to cache and track the get_page requests"""

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper that:
        - Checks if URL data is cached
        - Tracks how many times get_page is called
        """
        # Increment the URL access count
        redis_client.incr(f"count:{url}")
        
        # Sanitize URL for cache key
        cache_key = sanitize_url(url)
        
        # Check if the page is already cached
        cached_page = redis_client.get(cache_key)
        if cached_page:
            return cached_page.decode("utf-8")

        # If not cached, fetch from the URL and cache it with an expiration
        response = fn(url)
        redis_client.setex(cache_key, CACHE_EXPIRATION, response)
        return response

    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Fetches the content of a URL.

    Args:
        url (str): The URL to fetch
    Returns:
        str: HTML content of the page
    """
    response = requests.get(url)
    return response.text
