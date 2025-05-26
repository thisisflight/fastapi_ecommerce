from .category import router as category_router
from .product import router as product_router


all_routers = [
    category_router,
    product_router
]