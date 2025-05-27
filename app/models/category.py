from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend import Base


class Category(Base):
    category_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default="1")
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("category.category_id", ondelete="SET NULL"), nullable=True
    )
    products: Mapped[list["Product"]] = relationship(back_populates="category")  # noqa
    parent: Mapped["Category"] = relationship(remote_side=[category_id])
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
