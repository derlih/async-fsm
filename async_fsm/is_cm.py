import asyncio


def is_async_cm(obj):
    return asyncio.iscoroutinefunction(getattr(obj, '__aenter__', None)) \
        and asyncio.iscoroutinefunction(getattr(obj, '__aexit__', None))


def is_cm(obj):
    return callable(getattr(obj, '__enter__', None)) \
        and callable(getattr(obj, '__exit__', None))
