from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_mixin, mapped_column
from sqlalchemy.schema import MetaData
from sqlalchemy.types import BigInteger
from sqlalchemy_mixins.smartquery import SmartQueryMixin


class ModelBase(SmartQueryMixin, DeclarativeBase):
    __abstract__ = True
    __page_size__: int = 20
    __search_fields__: list[str] = []
    __repr_fields__: list[str] = []

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{field}={getattr(self, field)}' for field in self.__repr_fields__)})"


@declarative_mixin
class IDMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
