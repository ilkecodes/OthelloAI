from .clients import router as clients_router
from .trends import router as trends_router
from .content import router as content_router
from .campaigns import router as campaigns_router

__all__ = [
    'clients_router',
    'trends_router',
    'content_router',
    'campaigns_router',
]
