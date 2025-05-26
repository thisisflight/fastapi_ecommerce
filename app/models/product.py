from decimal import Decimal

from sqlalchemy import String, Integer, Float, Text, Numeric, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend import Base


class Product(Base):
    product_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), server_default="0.00")
    image_url: Mapped[str] = mapped_column(Text, nullable=True)
    stock: Mapped[int] = mapped_column(Integer, server_default="0")
    rating: Mapped[float] = mapped_column(Float, server_default="0.0")
    is_active: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.category_id'))
    category = relationship('Category', back_populates='products', uselist=False)

    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id', ondelete="SET NULL"))
    supplier = relationship('User', back_populates='products', uselist=False)
