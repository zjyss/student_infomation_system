from django.core.cache import cache


def set(message, decodemessage):
    cache.set(message, decodemessage, 60 * 60)


def get(key):
    return cache.get(key)


def _del(key):
    cache.delete(key)
    return True
