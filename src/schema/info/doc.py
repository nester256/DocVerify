from src.schema.base import Base, PageMixin


class DocumentCreateDTO(Base):
    title: str
    data: dict  # type: ignore
    version: int = 0


class DocumentCreatedResponse(Base):
    id: int
    status: str


class DocumentSignedResponse(Base):
    id: int
    signed_document_hash: str


class DocumentValidationResponse(Base):
    valid: bool


class DocumentGetDTO(Base):
    id: int
    original_document_hash: str | None = None
    original_document_path: str | None = None
    signed_document_hash: str | None = None
    signed_document_path: str | None = None
    status: str
    is_signed: bool


class DocumentFilters(PageMixin):
    is_signed: bool | None = None
