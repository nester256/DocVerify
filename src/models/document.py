from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_mixins.timestamp import TimestampsMixin

from .base import IDMixin, ModelBase


class Document(TimestampsMixin, ModelBase, IDMixin):
    __tablename__ = "docs"

    original_document_hash: Mapped[str] = mapped_column(nullable=True, unique=True)
    original_document_path: Mapped[str] = mapped_column(nullable=True)
    signed_document_hash: Mapped[str] = mapped_column(nullable=True, unique=True)
    signed_document_path: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)
    is_signed: Mapped[bool] = mapped_column(default=False)
