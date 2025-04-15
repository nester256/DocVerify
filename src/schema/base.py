from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T", bound=Base)


class Page(Base, Generic[T]):
    data: list[T]
    total_pages: int


class PageMixin(Base):
    page: int = Field(1, ge=1)


class SearchMixin(Base):
    search: str | None = Field(None, min_length=1)


class InfoMessage(Base):
    msg: str = "Success"
