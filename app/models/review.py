from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    SmallInteger,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend import Base


class Review(Base):
    review_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.user_id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("product.product_id", ondelete="CASCADE")
    )
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    grade: Mapped[int] = mapped_column(SmallInteger, server_default="1")
    is_active: Mapped[bool] = mapped_column(default=True)

    user = relationship("User", back_populates="review", uselist=False)
    product = relationship("Product", back_populates="reviews", uselist=False)

    __table_args__ = (
        CheckConstraint("grade >= 1 AND grade <= 5", name="ck_review_grade"),
        UniqueConstraint("user_id", "product_id", name="uq_review_user_id_product_id"),
    )
