try:
    from .cycuckoocache import LazyCuckooCache, CacheMissError, IsThreadsafe
except ImportError:
    from .pycuckoocache import LazyCuckooCache, CacheMissError, IsThreadsafe
