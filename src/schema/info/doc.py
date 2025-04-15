from src.schema.base import Base, PageMixin


class DocumentCreateDTO(Base):
    title: str
    content: str
    version: str | None = None


class DocumentCreatedResponse(Base):
    id: int
    original_document_hash: str
    link_to_download: str | None = None


class DocumentSignedResponse(Base):
    id: int
    signed_document_hash: str


class DocumentValidationResponse(Base):
    valid: bool


class DocumentGetDTO(Base):
    id: int
    original_document_hash: str
    original_document_path: str
    signed_document_hash: str | None = None
    signed_document_path: str | None = None
    is_signed: bool


class DocumentFilters(PageMixin):
    is_signed: bool | None = None
