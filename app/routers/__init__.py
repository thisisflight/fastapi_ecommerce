from .auth import router as auth_router
from .category import router as category_router
from .product import router as product_router
from .review import router as review_router

all_routers = [
    auth_router,
    category_router,
    product_router,
    review_router,
]
