try:
   from .cylrucache import CacheMissError, IsThreadsafe, LRUCache
except ImportError:
    from .pylrucache import CacheMissError, IsThreadsafe, LRUCache
