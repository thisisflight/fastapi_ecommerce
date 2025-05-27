from .auth import router as auth_router
from .category import router as category_router
from .product import router as product_router

all_routers = [
    auth_router,
    category_router,
    product_router,
]
