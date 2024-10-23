#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta
import redis

# Redis connection details (replace with your own)
redis_host = "localhost"
redis_port = 6379

# Cache expiration time in seconds
cache_expiration = 10

# Redis connection
redis_client = redis.Redis(host=redis_host, port=redis_port)


def get_page(url: str) -> str:
    """
    Fetches a webpage and caches the result with expiration.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The HTML content of the webpage.
    """

    cache_key = f"count:{url}"  # Key format for access count
    cached_data = redis_client.get(cache_key)

    if cached_data:
        # Increment access count for existing cache entry
        count = int(cached_data.decode()) + 1
        redis_client.set(cache_key, count, ex=cache_expiration)
        return cached_data.decode()

    # Cache miss, fetch data and store with expiration
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    redis_client.set(url, response.text, ex=cache_expiration)
    redis_client.set(cache_key, 1, ex=cache_expiration)  # Initialize count

    return response.text
