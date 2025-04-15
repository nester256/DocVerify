import hashlib
from typing import Any, Optional, Sequence

import aiofiles
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.document import Document
from src.repositories.base import Repository
from src.schema.info.doc import DocumentFilters


class DocumentRepository(Repository):
    @staticmethod
    async def create(session: AsyncSession, hash_: str, minio_path: str) -> Document:
        doc = Document(original_document_hash=hash_, original_document_path=minio_path, is_signed=False)
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return doc

    @staticmethod
    async def calculate_sha256(file_path: str) -> str:
        hash_func = hashlib.sha256()
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    async def get_by_hash(hash_: str, session: AsyncSession) -> Optional[Document]:
        result = await session.execute(select(Document).where(Document.original_document_hash == hash_))
        return result.scalar_one_or_none()

    @staticmethod
    async def add_signature(session: AsyncSession, doc: Document, storage_key: str, signed_hash: str) -> Document:
        doc.signed_document_hash = signed_hash
        doc.signed_document_path = storage_key
        doc.is_signed = True
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return doc

    @staticmethod
    async def get_by_signed_hash(hash_: str, session: AsyncSession) -> Optional[Document]:
        result = await session.execute(select(Document).where(Document.signed_document_hash == hash_))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        query_filters: DocumentFilters,
        limit: int,
        offset: int,
        session: AsyncSession,
    ) -> tuple[Sequence[Document], Any]:
        stmt = select(Document)

        if query_filters.is_signed is not None:
            stmt = stmt.where(Document.is_signed == query_filters.is_signed)

        total_stmt = stmt.with_only_columns(func.count()).order_by(None)
        stmt = stmt.offset(offset).limit(limit)

        result = await session.execute(stmt)
        docs = result.scalars().all()

        total_result = await session.execute(total_stmt)
        total_count = total_result.scalar_one()

        return docs, total_count
